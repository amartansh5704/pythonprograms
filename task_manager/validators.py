"""Validation utilities."""

from __future__ import annotations

from models import MAX_DESCRIPTION_LENGTH, MAX_TITLE_LENGTH, Priority, ValidationError


def validate_title(title: str) -> str:
    """Validate and return a cleaned title."""
    cleaned = title.strip()
    if not cleaned:
        raise ValidationError("Title cannot be empty or whitespace.")
    if len(cleaned) > MAX_TITLE_LENGTH:
        raise ValidationError(
            f"Title too long: {len(cleaned)} chars. Max: {MAX_TITLE_LENGTH}."
        )
    return cleaned


def validate_description(description: str) -> str:
    """Validate and return a cleaned description."""
    cleaned = description.strip()
    if len(cleaned) > MAX_DESCRIPTION_LENGTH:
        raise ValidationError(
            f"Description too long: {len(cleaned)} chars. "
            f"Max: {MAX_DESCRIPTION_LENGTH}."
        )
    return cleaned


def validate_tags(tags: list[str]) -> list[str]:
    """Validate, deduplicate, and clean tags."""
    cleaned_tags: list[str] = []
    seen: set[str] = set()

    for tag in tags:
        clean = tag.strip().lower()
        if not clean:
            continue
        # Allow letters, digits, hyphens, underscores
        allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789-_")
        if not all(c in allowed_chars for c in clean):
            raise ValidationError(
                f"Tag '{clean}' has invalid characters. "
                "Use only letters, digits, hyphens, underscores."
            )
        if clean not in seen:
            seen.add(clean)
            cleaned_tags.append(clean)

    return cleaned_tags


def validate_priority_string(priority_str: str) -> Priority:
    """Convert string to Priority enum."""
    normalized = priority_str.strip().lower()
    try:
        return Priority(normalized)
    except ValueError as exc:
        valid = [p.value for p in Priority]
        raise ValidationError(
            f"Invalid priority '{priority_str}'. Choose from: {valid}"
        ) from exc