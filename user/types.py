import graphene


class UserProfessionInput(graphene.InputObjectType):
    user = graphene.ID()
    designation_title = graphene.String(required=True)
    designation_id = graphene.Int()
    income_range_id = graphene.Int()
    created_at = graphene.Date()
