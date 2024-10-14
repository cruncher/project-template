from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import Tag


#Managing tags as snippets
#
# To manage all the tags used in a project, 
# you can register the Tag model as a snippet 
# to be managed via the Wagtail admin. 
# This will allow you to have a tag admin interface 
# within the main menu in which you can add, 
# edit or delete your tags.
#
# Tags that are removed from a content don’t get deleted 
# from the Tag model and will still be shown in typeahead tag completion.
# So having a tag interface is a great way to 
# completely get rid of tags you don’t need.

class TagsSnippetViewSet(SnippetViewSet):
    panels = [FieldPanel("name")]  # only show the name field
    model = Tag
    icon = "tag"  # change as required
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ["name", "slug"]
    search_fields = ("name",)

register_snippet(TagsSnippetViewSet)