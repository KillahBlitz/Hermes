import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from googleapiclient.discovery import build
from src.models.request.services import CalendarEventCreateRequest, CalendarEventUpdateRequest
from src.utils.google_credentials import build_google_credentials

logger = logging.getLogger("hermes-api.calendar")


class CalendarService:
    """Service layer for Google Calendar API v3 interactions."""

    def __init__(self, access_token: str):
        creds = build_google_credentials(access_token)
        self.service = build("calendar", "v3", credentials=creds, cache_discovery=False)

    def _format_event(self, item: Dict[str, Any]) -> Dict[str, Any]:
        start_obj = item.get("start", {})
        end_obj = item.get("end", {})
        is_all_day = "date" in start_obj

        start_val = start_obj.get("dateTime") or start_obj.get("date") or ""
        end_val = end_obj.get("dateTime") or end_obj.get("date") or ""

        attendees = [
            att.get("email") for att in item.get("attendees", []) if att.get("email")
        ]

        return {
            "id": item.get("id"),
            "summary": item.get("summary") or "(Sin título)",
            "description": item.get("description"),
            "location": item.get("location"),
            "start": start_val,
            "end": end_val,
            "is_all_day": is_all_day,
            "html_link": item.get("htmlLink"),
            "status": item.get("status", "confirmed"),
            "color_id": item.get("colorId"),
            "attendees": attendees,
            "created": item.get("created"),
            "updated": item.get("updated"),
        }

    def list_events(
        self,
        time_min: Optional[str] = None,
        time_max: Optional[str] = None,
        q: Optional[str] = None,
        max_results: int = 100,
        calendar_id: str = "primary",
    ) -> List[Dict[str, Any]]:
        """Lista eventos del calendario dentro de un rango de tiempo."""
        try:
            params: Dict[str, Any] = {
                "calendarId": calendar_id,
                "singleEvents": True,
                "orderBy": "startTime",
                "maxResults": max_results,
            }
            if time_min:
                params["timeMin"] = time_min
            if time_max:
                params["timeMax"] = time_max
            if q:
                params["q"] = q

            res = self.service.events().list(**params).execute()
            items = res.get("items", [])
            return [self._format_event(item) for item in items]
        except Exception as e:
            logger.error(f"Error listando eventos de Google Calendar: {e}")
            raise

    def get_event(self, event_id: str, calendar_id: str = "primary") -> Optional[Dict[str, Any]]:
        """Obtiene el detalle de un evento específico."""
        try:
            item = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
            return self._format_event(item)
        except Exception as e:
            logger.error(f"Error obteniendo evento {event_id}: {e}")
            raise

    def create_event(
        self,
        req: CalendarEventCreateRequest,
        calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """Crea un nuevo evento en Google Calendar."""
        try:
            body: Dict[str, Any] = {
                "summary": req.summary.strip(),
            }
            if req.description:
                body["description"] = req.description.strip()
            if req.location:
                body["location"] = req.location.strip()
            if req.color_id:
                body["colorId"] = req.color_id

            if req.is_all_day:
                # Todo el día espera formato YYYY-MM-DD
                body["start"] = {"date": req.start_time[:10]}
                body["end"] = {"date": req.end_time[:10]}
            else:
                body["start"] = {"dateTime": req.start_time}
                body["end"] = {"dateTime": req.end_time}

            if req.attendees:
                body["attendees"] = [{"email": email.strip()} for email in req.attendees if email.strip()]

            item = self.service.events().insert(calendarId=calendar_id, body=body).execute()
            return self._format_event(item)
        except Exception as e:
            logger.error(f"Error creando evento en Google Calendar: {e}")
            raise

    def update_event(
        self,
        event_id: str,
        req: CalendarEventUpdateRequest,
        calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """Actualiza un evento existente en Google Calendar."""
        try:
            body: Dict[str, Any] = {}
            if req.summary is not None:
                body["summary"] = req.summary.strip()
            if req.description is not None:
                body["description"] = req.description.strip()
            if req.location is not None:
                body["location"] = req.location.strip()
            if req.color_id is not None:
                body["colorId"] = req.color_id

            if req.start_time is not None or req.end_time is not None or req.is_all_day is not None:
                is_all_day = req.is_all_day if req.is_all_day is not None else False
                if is_all_day:
                    if req.start_time:
                        body["start"] = {"date": req.start_time[:10]}
                    if req.end_time:
                        body["end"] = {"date": req.end_time[:10]}
                else:
                    if req.start_time:
                        body["start"] = {"dateTime": req.start_time}
                    if req.end_time:
                        body["end"] = {"dateTime": req.end_time}

            if req.attendees is not None:
                body["attendees"] = [{"email": email.strip()} for email in req.attendees if email.strip()]

            item = self.service.events().patch(
                calendarId=calendar_id,
                eventId=event_id,
                body=body
            ).execute()
            return self._format_event(item)
        except Exception as e:
            logger.error(f"Error actualizando evento {event_id}: {e}")
            raise

    def delete_event(self, event_id: str, calendar_id: str = "primary") -> bool:
        """Elimina un evento de Google Calendar."""
        try:
            self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error eliminando evento {event_id}: {e}")
            raise

    def quick_add_event(self, text: str, calendar_id: str = "primary") -> Dict[str, Any]:
        """Crea un evento rápido a partir de lenguaje natural."""
        try:
            item = self.service.events().quickAdd(calendarId=calendar_id, text=text.strip()).execute()
            return self._format_event(item)
        except Exception as e:
            logger.error(f"Error en quickAdd de Google Calendar: {e}")
            raise
