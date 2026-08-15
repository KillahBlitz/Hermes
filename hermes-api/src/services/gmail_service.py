import logging
import base64
from typing import Any, Dict, List, Optional, Tuple
from googleapiclient.discovery import build
from src.utils.google_credentials import build_google_credentials

logger = logging.getLogger("hermes-api.gmail")


class GmailService:
    """Service layer for Gmail API v1 interactions."""

    def __init__(self, access_token: str):
        creds = build_google_credentials(access_token)
        self.service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    # ── List Priority Emails ──

    def list_priority_emails(
        self,
        filter_type: str = "all",
        search_query: str = "",
        page_token: Optional[str] = None,
        max_results: int = 10,
    ) -> Dict[str, Any]:
        """
        List emails that are starred and/or important.
        filter_type: 'all' | 'starred' | 'important'
        """
        query_parts = []
        if filter_type == "starred":
            query_parts.append("is:starred")
        elif filter_type == "important":
            query_parts.append("is:important")
        else:
            query_parts.append("(is:starred OR is:important)")

        if search_query:
            query_parts.append(search_query)

        q = " ".join(query_parts)

        try:
            params: Dict[str, Any] = {
                "userId": "me",
                "q": q,
                "maxResults": max_results,
            }
            if page_token:
                params["pageToken"] = page_token

            response = self.service.users().messages().list(**params).execute()
            messages = response.get("messages", [])
            next_page_token = response.get("nextPageToken")
            result_size = response.get("resultSizeEstimate", 0)

            email_summaries = []
            for msg in messages:
                detail = self._get_message_summary(msg["id"])
                if detail:
                    email_summaries.append(detail)

            return {
                "emails": email_summaries,
                "next_page_token": next_page_token,
                "result_size_estimate": result_size,
            }
        except Exception as e:
            logger.error(f"Error listing priority emails: {e}")
            raise

    def _get_message_summary(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get minimal headers for list display."""
        try:
            msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="metadata", metadataHeaders=["From", "Subject", "Date"])
                .execute()
            )
            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            labels = msg.get("labelIds", [])

            sender_full = headers.get("From", "")
            sender_name, sender_email = self._parse_sender(sender_full)

            return {
                "id": msg["id"],
                "thread_id": msg.get("threadId", ""),
                "sender": sender_name,
                "sender_email": sender_email,
                "subject": headers.get("Subject", "(Sin asunto)"),
                "snippet": msg.get("snippet", ""),
                "is_starred": "STARRED" in labels,
                "is_important": "IMPORTANT" in labels,
                "date": headers.get("Date", ""),
            }
        except Exception as e:
            logger.warning(f"Error fetching summary for message {message_id}: {e}")
            return None

    # ── Get Email Detail ──

    def get_email_detail(self, message_id: str) -> Dict[str, Any]:
        """Get full email content including body and attachments."""
        try:
            msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )
            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            labels = msg.get("labelIds", [])

            sender_full = headers.get("From", "")
            sender_name, sender_email = self._parse_sender(sender_full)

            body_html, body_text = self._extract_body(msg.get("payload", {}))
            attachments = self._extract_attachments(msg.get("payload", {}), message_id)

            return {
                "id": msg["id"],
                "thread_id": msg.get("threadId", ""),
                "sender": sender_name,
                "sender_email": sender_email,
                "recipients": headers.get("To", ""),
                "subject": headers.get("Subject", "(Sin asunto)"),
                "date": headers.get("Date", ""),
                "body_html": body_html,
                "body_text": body_text,
                "labels": labels,
                "attachments": attachments,
            }
        except Exception as e:
            logger.error(f"Error fetching email detail {message_id}: {e}")
            raise

    # ── Trash Email ──

    def trash_email(self, message_id: str) -> bool:
        """Move an email to trash."""
        try:
            self.service.users().messages().trash(userId="me", id=message_id).execute()
            logger.info(f"Email {message_id} moved to trash")
            return True
        except Exception as e:
            logger.error(f"Error trashing email {message_id}: {e}")
            raise

    # ── Helpers ──

    @staticmethod
    def _parse_sender(sender_full: str) -> Tuple[str, str]:
        """Parse 'Name <email@domain.com>' into (name, email)."""
        if "<" in sender_full and ">" in sender_full:
            name = sender_full.split("<")[0].strip().strip('"')
            email = sender_full.split("<")[1].split(">")[0].strip()
            return name or email, email
        return sender_full, sender_full

    def _extract_body(self, payload: Dict) -> Tuple[Optional[str], Optional[str]]:
        """Recursively extract HTML and plain text body from payload."""
        body_html = None
        body_text = None

        mime_type = payload.get("mimeType", "")
        body_data = payload.get("body", {}).get("data")

        if body_data:
            decoded = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="replace")
            if "html" in mime_type:
                body_html = decoded
            else:
                body_text = decoded

        for part in payload.get("parts", []):
            h, t = self._extract_body(part)
            if h:
                body_html = h
            if t:
                body_text = t

        return body_html, body_text

    def _extract_attachments(self, payload: Dict, message_id: str) -> List[Dict]:
        """Extract attachment metadata from payload."""
        attachments = []
        for part in payload.get("parts", []):
            filename = part.get("filename")
            body = part.get("body", {})
            attachment_id = body.get("attachmentId")
            if filename and attachment_id:
                attachments.append({
                    "filename": filename,
                    "mime_type": part.get("mimeType", "application/octet-stream"),
                    "size": body.get("size", 0),
                    "attachment_id": attachment_id,
                })
            # Recurse into nested parts
            if part.get("parts"):
                attachments.extend(self._extract_attachments(part, message_id))
        return attachments
