from graphene import Interface, String, ID, Boolean


class Viewer(Interface):
    id = ID()
    token = String()
    avatar = String()
    hasWallet = String()
    didRequest = Boolean(required=True)
