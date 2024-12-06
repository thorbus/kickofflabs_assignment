from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEventOwner(BasePermission):
    '''
    To Check if the logged in user is the owner of the event
    '''

    message = "User can only create, update, or delete a event, if it is a owner"
   
    def has_permission(self, request, view):
                
        return True

    def has_object_permission(self, request, view, obj):
        
        if view.action in [ "retrieve", "partial_update", "update", "destroy"]:
            self.message = "Logged in user is not the event owner"
            return obj.user == request.user

        if view.action in ["list"]:
            return True
        
        return False