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
        self.urls=[]
    def start_section(self, attrs):
        attr = [v for k, v in attrs if k=='data-score']
        if attr:
            self.urls.extend(attr)

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
                         #'active': False})
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
        if confirm.urls[0] == 'correct':
            content.append(add_edit_tool(con,course,descriptor[x]))
    import logging
    log = logging.getLogger("tracking")
    #log.debug("content===============================\n:"+str(reverse('jump_to_id',args=(course.id,'8f563e9f334f4f50a9c6d32ee3161b77')))+"\n===========================")
    log.debug("content===============================\n:"+str(location)+"\n===========================")
    return content

   

