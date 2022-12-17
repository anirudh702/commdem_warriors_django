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
    def success_with_commitment_update(cls, data, message,isCommitmentUpdated):
        """
        Common success method for API response
        """
        return {"success": True, "data": data, "message": message,"isCommitmentUpdated" : isCommitmentUpdated}

    @classmethod
    def success_for_referral_code(cls, message,referralCode):
        """
        Common success method for API response
        """
        return {"success": True,"referral_code" : referralCode, "message": message}

    @classmethod
    def success_without_data(cls, message):
        """
        Common success_without_data method for API response
        """
        return {"success": True, "message": message}

    @classmethod
    def success_without_data_with_commitment_update(cls, message,isCommitmentUpdated):
        """
        Common success_without_data method for API response
        """
        return {"success": True, "message": message,'isCommitmentUpdated' : isCommitmentUpdated}

    @classmethod
    def error(cls, error):
        """
        Common error method for API response
        """
        return {"success": False, "message": error}

    @classmethod
    def user_subscribed(cls, message,is_subscribed,is_admin):
        """
        Common error method for API response
        """
        return {"success": True, "message": message, "is_subscribed" : is_subscribed,'is_admin' : is_admin}