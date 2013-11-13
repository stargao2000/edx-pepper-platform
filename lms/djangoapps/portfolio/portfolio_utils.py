from xmodule.modulestore.django import modulestore
from xmodule.modulestore import Location
from courseware.module_render import toc_for_course, get_module_for_descriptor
from courseware.model_data import FieldDataCache
from courseware.views import jump_to_id
from django.core.urlresolvers import reverse
from sgmllib import SGMLParser
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')
class Get_confirm(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.score_urls=[]
        self.state_urls=[]
    def start_section(self, attrs):
        score_attr = [v for k, v in attrs if k=='data-score']
        state_attr = [v for k, v in attrs if k=='data-state']
        if score_attr:
            self.score_urls.extend(score_attr)
        if state_attr:
            self.state_urls.extend(state_attr)

def add_edit_tool(data, course, descriptor):
    return '''<div>{0}<a class="blue_btn" href="{1}">Edit in Course</a>&nbsp;&nbsp;<a class="orange_btn" href="#">View & Join Discussion</a></div>'''.format(data,reverse('jump_to_id',args=(course.id,descriptor.location[4])))

def get_chaper_for_course(request, course, active_chapter):
    model_data_cache = FieldDataCache.cache_for_descriptor_descendents(
            course.id, request.user, course, depth=2)
    course_module = get_module_for_descriptor(request.user, request, course, model_data_cache, course.id)
    if course_module is None:
        return None

    chapters = list()
    for chapter in course_module.get_display_items():
        chapters.append({'display_name': chapter.display_name_with_default,
                         'url_name': chapter.url_name,
                         'active': chapter.url_name == active_chapter})
    return chapters
def get_module_combinedopenended(request, course, location, isupload):
    location = course.location[0]+'://'+course.location[1]+'/'+course.location[2]+'/chapter/'+location
    section_descriptor = modulestore().get_instance(course.id, location, depth=None)
    field_data_cache = FieldDataCache.cache_for_descriptor_descendents(course.id, request.user, section_descriptor, depth=None)
    descriptor = modulestore().get_instance_items(course.id, location,'combinedopenended',depth=None)
    content = []
    
    for x in range(len(descriptor)):
        module = get_module_for_descriptor(request.user, request, descriptor[x], field_data_cache, course.id,
                                         position=None, wrap_xmodule_display=True, grade_bucket_type=None,
                                         static_asset_path='')
        con = module.runtime.render(module, None, 'student_view').content
        confirm = Get_confirm()
        confirm.feed(con)
        if confirm.score_urls[0] == 'correct' and confirm.state_urls[0] == 'done':
            content.append(add_edit_tool(con,course,descriptor[x]))

    return content

   

