from app.core.logging import logger
from app.schemas.lokalise import (
    Comment,
    CommentCreateResponse,
    CommentFilters,
    CommentsCreate,
    KeyCommentsResponse,
)

from .base import LokaliseBaseService


class LokaliseCommentsService(LokaliseBaseService):
    """Service for Lokalise comments operations."""

    async def get_key_comments(
        self,
        project_id: str,
        key_id: int,
        filters: CommentFilters | None = None,
    ) -> KeyCommentsResponse:
        """
        Retrieve all comments for a specific key in a project.

        Args:
            project_id: Lokalise project ID
            key_id: Unique identifier of the key
            filters: Optional filters for comments

        Returns:
            KeyCommentsResponse with project_id, comments array, and total count

        Raises:
            HTTPException: For API errors, rate limits, or invalid tokens
        """
        try:
            # Configure API parameters
            params = {}

            if filters:
                if filters.limit is not None:
                    params["limit"] = min(filters.limit, 5000)  # Respect max limit
                if filters.page is not None:
                    params["page"] = filters.page

            # Get comments from Lokalise
            logger.info(
                f"Fetching comments for key {key_id} in project {project_id} with params: {params}"
            )
            comments_response = self.client.key_comments(project_id, key_id, params)
            logger.info(
                f"Retrieved {len(comments_response.items) if comments_response.items else 0} comments from Lokalise"
            )

            if not comments_response.items:
                logger.warning(
                    f"No comments found for key {key_id} in project {project_id}"
                )
                return KeyCommentsResponse(
                    project_id=project_id,
                    comments=[],
                    total_count=0,
                )

            # Format the response data
            result_comments = []
            processed_count = 0

            for comment_data in comments_response.items:  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                processed_count += 1
                comment_id = self._safe_get_attr(comment_data, "comment_id", 0)
                logger.debug(f"Processing comment {processed_count}: {comment_id}")

                result_comments.append(self._build_comment_object(comment_data))

            # Get total count from response headers or metadata
            total_count = len(result_comments)
            if hasattr(comments_response, "total_count"):
                total_count = getattr(comments_response, "total_count", total_count)

            logger.info(
                f"Successfully processed {len(result_comments)} comments for key {key_id} in project {project_id}"
            )

            return KeyCommentsResponse(
                project_id=project_id,
                comments=result_comments,
                total_count=total_count,
            )

        except Exception as e:
            self._handle_api_error(
                e, "fetching key comments", f"key {key_id} in project {project_id}"
            )
            # Return empty response structure on error (this won't be reached due to exception)
            return KeyCommentsResponse(
                project_id=project_id,
                comments=[],
                total_count=0,
            )

    async def create_key_comments(
        self,
        project_id: str,
        key_id: int,
        create_data: CommentsCreate,
    ) -> CommentCreateResponse:
        """
        Create comments for a specific key in a project.

        Args:
            project_id: Lokalise project ID
            key_id: Unique identifier of the key
            create_data: CommentsCreate schema with the comments to create

        Returns:
            CommentCreateResponse with project_id and created comment

        Raises:
            HTTPException: For API errors, rate limits, invalid tokens, or validation errors
        """
        try:
            # Prepare the comments data for Lokalise SDK
            lokalise_comments = []

            for comment in create_data.comments:
                comment_data = {
                    "comment": comment.comment,
                }
                lokalise_comments.append(comment_data)

            # Create comments in Lokalise
            logger.info(
                f"Creating {len(create_data.comments)} comments for key {key_id} in project {project_id}"
            )
            logger.debug(f"Comments payload: {lokalise_comments}")

            # Use the correct SDK method - assuming it's create_key_comments
            created_comments = self.client.create_key_comments(
                project_id, key_id, lokalise_comments
            )
            logger.info(
                f"Successfully created comments in Lokalise for key {key_id} in project {project_id}"
            )

            # According to the API spec, the response contains a single comment object
            # We'll take the first created comment or the response directly if it's a single comment
            if hasattr(created_comments, "items") and created_comments.items:
                # If response has items array, take the first one
                comment_data = created_comments.items[0]
            else:
                # If response is a single comment object
                comment_data = created_comments

            created_comment = self._build_comment_object(comment_data)

            logger.info(
                f"Successfully processed created comment for key {key_id} in project {project_id}"
            )

            return CommentCreateResponse(
                project_id=project_id,
                comment=created_comment,
            )

        except Exception as e:
            self._handle_api_error(
                e, "creating key comments", f"key {key_id} in project {project_id}"
            )
            # This return will never be reached due to _handle_api_error raising HTTPException
            return CommentCreateResponse(
                project_id=project_id,
                comment=Comment(
                    comment_id=0,
                    key_id=key_id,
                    comment="",
                    added_by=0,
                    added_by_email="",
                    added_at="",
                    added_at_timestamp=0,
                ),
            )

    def _build_comment_object(self, comment_data) -> Comment:
        """Build a Comment object from Lokalise API response data."""
        return Comment(
            comment_id=self._ensure_int(
                self._safe_get_attr(comment_data, "comment_id", 0)
            ),
            key_id=self._ensure_int(self._safe_get_attr(comment_data, "key_id", 0)),
            comment=str(self._safe_get_attr(comment_data, "comment", "")),
            added_by=self._ensure_int(self._safe_get_attr(comment_data, "added_by", 0)),
            added_by_email=str(self._safe_get_attr(comment_data, "added_by_email", "")),
            added_at=str(self._safe_get_attr(comment_data, "added_at", "")),
            added_at_timestamp=self._ensure_int(
                self._safe_get_attr(comment_data, "added_at_timestamp", 0)
            ),
        )


# Create singleton instance
lokalise_comments_service = LokaliseCommentsService()
