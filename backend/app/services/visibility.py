"""Visibility filtering service for GM/Player modes."""

from typing import Any, Literal

ViewMode = Literal["gm", "player"]


class VisibilityService:
    """Service for applying GM/Player visibility rules."""

    @staticmethod
    def filter_scope(scope: str, view_mode: ViewMode) -> bool:
        """
        Check if entity with given scope should be visible in view mode.

        Rules:
        - GM mode: sees everything (public, gm, player)
        - Player mode: sees public + player (hides gm)

        Args:
            scope: Entity scope (public|gm|player)
            view_mode: Current view mode (gm|player)

        Returns:
            True if entity should be visible
        """
        if view_mode == "gm":
            return True
        # Player mode: hide gm-only content
        return scope in ("public", "player")

    @staticmethod
    def filter_notes_gm(data: dict[str, Any], view_mode: ViewMode) -> dict[str, Any]:
        """
        Filter notes_gm field from response data based on view mode.

        Args:
            data: Response data dictionary
            view_mode: Current view mode (gm|player)

        Returns:
            Filtered data with notes_gm removed/nullified in player mode
        """
        if view_mode == "player" and "notes_gm" in data:
            data["notes_gm"] = None
        return data

    @staticmethod
    def get_allowed_scopes(view_mode: ViewMode) -> tuple[str, ...]:
        """
        Get list of allowed scopes for the view mode.

        Args:
            view_mode: Current view mode (gm|player)

        Returns:
            Tuple of allowed scope values
        """
        if view_mode == "gm":
            return ("public", "gm", "player")
        return ("public", "player")
