from rest_framework import permissions
from django.contrib.auth.models import Group


class IsManagerOrEmployee(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        manager_group = Group.objects.get(name="warehouse manager")
        employee_group = Group.objects.get(name="warehouse employee")

        if manager_group in request.user.groups.all() or employee_group in request.user.groups.all():
            # DELETE request provided only for group "warehouse manager"
            False if request.method == "DELETE" and not manager_group in request.user.groups.all() else True
        else:
            return False

    def has_permission(self, request, view):
        manager_group = Group.objects.get(name="warehouse manager")
        employee_group = Group.objects.get(name="warehouse employee")
        return True if manager_group in request.user.groups.all() or employee_group in request.user.groups.all() else False
