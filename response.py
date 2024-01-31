"""
Common response class for whole project
"""


class Response:
    """
    Common response class for API response
    """

    @classmethod
    def success(cls, data, message):
        """
        Common success method for API response
        """
        return {"success": True, "data": data, "message": message}

    @classmethod
    def success_for_getting_commitments(cls, data, commitment_category_data, message):
        """
        Common success method for API response
        """
        return {
            "success": True,
            "data": data,
            "commitment_category_data": commitment_category_data,
            "message": message,
        }

    @classmethod
    def success_for_get_reviews(
        cls, data, message, can_user_submit_review, next_review_date
    ):
        """
        Common success method for API response
        """
        return {
            "success": True,
            "data": data,
            "message": message,
            "can_user_submit_review": can_user_submit_review,
            "next_review_date": next_review_date,
        }

    @classmethod
    def success_with_commitment_update(
        cls, data, commitment_category_data, message, isCommitmentUpdated
    ):
        """
        Common success method for API response
        """
        return {
            "success": True,
            "data": data,
            "commitment_category_data": commitment_category_data,
            "message": message,
            "isCommitmentUpdated": isCommitmentUpdated,
        }

    @classmethod
    def success_for_referral_code(cls, message, referralCode):
        """
        Common success method for API response
        """
        return {"success": True, "referral_code": referralCode, "message": message}

    @classmethod
    def success_without_data(cls, message):
        """
        Common success_without_data method for API response
        """
        return {"success": True, "message": message}

    @classmethod
    def success_without_data_with_commitment_update(cls, message, isCommitmentUpdated):
        """
        Common success_without_data method for API response
        """
        return {
            "success": True,
            "message": message,
            "isCommitmentUpdated": isCommitmentUpdated,
        }

    @classmethod
    def success_without_data_with_is_commitment_added_last_week(
        cls, message, is_commitment_added_last_week
    ):
        """
        Common success_without_data method for API response
        """
        return {
            "success": True,
            "message": message,
            "is_commitment_added_last_week": is_commitment_added_last_week,
        }

    @classmethod
    def error(cls, error):
        """
        Common error method for API response
        """
        return {"success": False, "message": error}

    @classmethod
    def common_subscription_message(
        cls, message, is_free_trial, is_subscription_active
    ):
        """
        Common error method for API response
        """
        return {
            "success": False,
            "message": message,
            "is_free_trial": is_free_trial,
            "is_subscription_active": is_subscription_active,
        }

    @classmethod
    def user_subscribed(
        cls,
        message,
        is_subscribed,
        is_admin,
        subscription_end_date="",
        is_todays_review_added=False,
    ):
        """
        Common error method for API response
        """
        return {
            "success": True,
            "message": message,
            "is_subscribed": is_subscribed,
            "is_admin": is_admin,
            "subscription_end_date": subscription_end_date,
            "is_todays_review_added": is_todays_review_added,
        }

    @classmethod
    def free_trial_not_started(
        cls,
        message,
        is_subscribed,
        is_admin,
        subscription_end_date="",
        is_todays_review_added=False,
        free_trial_not_started=True,
    ):
        """
        Common error method for API response
        """
        return {
            "success": True,
            "message": message,
            "is_subscribed": is_subscribed,
            "is_admin": is_admin,
            "subscription_end_date": subscription_end_date,
            "is_todays_review_added": is_todays_review_added,
            "free_trial_not_started": free_trial_not_started,
        }
