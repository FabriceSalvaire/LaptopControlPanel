####################################################################################################
# 
# LaptopControlPanel - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
#
# This code was inspired from http://code.google.com/p/pyredminews
# 
####################################################################################################

####################################################################################################

import urllib
import urllib2

from xml.dom import minidom, getDOMImplementation

####################################################################################################
#
# http://www.redmine.org/projects/redmine/wiki/Rest_api
# http://www.redmine.org/projects/redmine/wiki/Rest_Projects
# http://www.redmine.org/projects/redmine/wiki/Rest_Issues
#
# http://code.google.com/p/pyactiveresource/
# http://code.google.com/p/pyredminews/
#
# GET /issues.json
# http://docs.python.org/library/json.html#module-json
#
# http://intranet/redmine-it/public/projects/LaptopControlPanel.xml
# <project>
#   <id>1</id>
#   <name>LaptopControlPanel</name>
#   <identifier>project_identifier</identifier>
#   <description/>
#   <homepage/>
#   <created_on>Tue Feb 02 16:35:34 +0100 2010</created_on>
#   <updated_on>Tue Feb 02 16:35:34 +0100 2010</updated_on>
#   <trackers>
#     <tracker name="Task" id="4"/>
#     <tracker name="Bug" id="1"/>
#     <tracker name="Feature" id="2"/>
#     <tracker name="Support" id="3"/>
#     <tracker name="Meeting" id="5"/>
#     <tracker name="Document" id="7"/>
#     <tracker name="Unit Test" id="9"/>
#     </trackers>
# </project>
# 
# http://intranet/redmine-it/public/issues/173.xml
# <issue>
#   <id>173</id>
#   <project name="LaptopControlPanel" id="1"/>
#   <tracker name="Feature" id="2"/>
#   <status name="New" id="1"/>
#   <priority name="Normal" id="4"/>
#   <author name="Fabrice Salvaire" id="3"/>
#   <assigned_to name="Fabrice Salvaire" id="3"/>
#   <fixed_version name="v0.6.0" id="3"/>
#   <subject>
#   Add the possibility to choose image processing pipeline
#   </subject>
#   <description/>
#   <start_date>2010-05-11</start_date>
#   <due_date/>
#   <done_ratio>0</done_ratio>
#   <estimated_hours/>
#   <spent_hours>0.0</spent_hours>
#   <created_on>Tue May 11 12:58:36 +0200 2010</created_on>
#   <updated_on>Tue May 11 12:58:36 +0200 2010</updated_on>
#   <relations>
#   </relations>
# </issue>
# 
# http://intranet/redmine-it/public/issues.xml
# <issues type="array">
#   <issue>
#   ...
#   </issue>
# ...
#
# http://intranet/redmine-it/public/projects/LaptopControlPanel/issues.xml
# 
####################################################################################################

####################################################################################################

class PutRequest(urllib2.Request):

    '''Extend the request to handle PUT command.
    '''

    def get_method(self):
        return 'PUT'

####################################################################################################

class DeleteRequest(urllib2.Request):
    
    '''Extend the request to handle DELETE command.
    '''
    
    def get_method(self):
        return 'DELETE'

####################################################################################################

class RedmineRest:

    '''Redmine REST API.
    '''

    # Status ID from a default install
    ISSUE_STATUS_ID_NEW = 1
    ISSUE_STATUS_ID_RESOLVED = 3
    ISSUE_STATUS_ID_CLOSED = 5

    ##############################################

    def __init__(self, url, key=None, user_name=None, password=None):

        self._url = url

        # Create a password manager
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None,
                                      self._url,
                                      user_name or key,
                                      password or '',
                                      )

        handler = urllib2.HTTPBasicAuthHandler(password_manager)

        self._opener = urllib2.build_opener(handler)
        self._opener.open(url)
        urllib2.install_opener(self._opener)

    ##############################################

    def open_page(self, page, parameters={}, dom=None, http_request=urllib2.Request):

        '''Open a page from the server.
        '''

        if parameters is not None:
            url_data = '?' + urllib.urlencode(parameters)
        else:
            url_data = ''

        full_url = self._url + '/' + page
        print 'Redmine REST - Open page:', full_url

        self._opener.open(full_url)

        request = http_request(full_url + url_data)

        # Get the data and return XML object
        if dom is not None:
            request.add_header('Content-Type', 'text/xml')
            response = urllib2.urlopen(request, dom.toxml())
        else:
            response = urllib2.urlopen(request)
        xml_string = response.read()
        print '  XML document:\n', xml_string

        try:
            # return minidom.parse(response)
            return minidom.parseString(xml_string)
        except:
            return response.read() # ?

    ##############################################
 
    def post(self, page, dom, parameters=None):

        '''Post an XML object to the server.
        '''

        print 'Post:', page
        print dom.toxml()

        return self.open_page(page, parameters, dom)
 
    ##############################################
 
    def put(self, page, dom, parameters=None):

        '''Put an XML object on the server.
        '''

        return self.open_page(page, parameters, dom, http_request=self.PutRequest)
 
    ##############################################
 
    def delete(self, page):

        '''Delete a given object on the server.
        '''

        return self.open_page(page, http_request=self.DeleteRequest)
 
    ##############################################
 
    def dom_to_dict(self, dom, container):

        '''Parse the DOM into a Python dict.
        '''

        # Todo: correctly parse nested child nodes
 
        data = {}
        element = dom.getElementsByTagName(container)[0]
        for child in element.childNodes:
            if child.hasChildNodes():
                data[child.nodeName] = child.firstChild.nodeValue
 
        return data

    ##############################################
 
    def create_xml_document(self, root_element_name):

        '''Create a new XML document with a child element object having the given
        root_element_name.
        '''

        return getDOMImplementation().createDocument(None, root_element_name, None)
 
    ##############################################
 
    def add_key_to_xml_document(self, xml_document, xml_node, key, value):

        '''Add a key/value pair to a given xml_document at the xml_node location.
        '''

        element = xml_document.createElement(str(key))
        element.appendChild(xml_document.createTextNode(str(value)))
        xml_node.appendChild(element)
 
    ##############################################
 
    def dict_to_xml(self, root_element_name, data):

        '''Convert the dict to a new XML document with a child element object having the given
        root_element_name.
        '''

        xml_document = self.create_xml_document(root_element_name)
        for key in data:
            self.add_key_to_xml_document(xml_document, xml_document.firstChild, key, data[key])

        print 'XML document:', xml_document.toxml()
 
        return xml_document
 
    ##############################################
 
    def parse_project(self, dom):

        ''' Parse a project DOM'''

        project_dict = self.dom_to_dict(dom, 'project')
 
        return project_dict
 
    ##############################################
 
    def parse_issue(self, dom):

        ''' Parse an issue DOM'''

        issue_dict = self.dom_to_dict(dom, 'issue')

        return issue_dict
 
    ##############################################

    def get_project(self, project_name):

        '''Return a dictionary for the given project name
        '''

        return RedmineProject(self, self.open_page('projects/' + project_name + '.xml'))

    ##############################################
 
    def get_issue(self, issue_id):

        '''Return a dictionary for the given issue
        '''

        return self.parse_issue(self.open_page('issues/' + str(issue_id) + '.xml'))
 
    ##############################################
 
    def new_issue_from_dict(self, data):

        '''Create a new issue from a dictionary
        '''

        xml_document = self.dict_to_xml('issue', data)

        return self.parse_issue(self.post('issues.xml', xml_document))
 
    ##############################################
 
    def update_issue_from_dict(self, issue_id, data):

        '''Update an issue with the given issue_id using fields from the passed dictionary.
        '''

        xml_document = self.dict_to_xml('issue', data)

        return self.put('issues/' + str(issue_id) + '.xml', xml)
 
    ##############################################
 
    def close_issue(self, issue_id):

        '''Close an issue by setting the status to ISSUE_STATUS_ID_CLOSED.
        '''

        return self.update_issue_from_dict(issue_id,
                                           {'status_id':self.ISSUE_STATUS_ID_CLOSED})
 
    ##############################################
 
    def resolve_issue(self, issue_id):

        '''Close an issue by setting the status to ISSUE_STATUS_ID_RESOLVED.
        '''

        return self.update_issue_from_dict(issue_id,
                                           {'status_id':self.ISSUE_STATUS_ID_RESOLVED})
 
    ##############################################
 
#   def delete_issue(self, issue_id):
#
#       '''Delete an issue with the given ID.  Note that the proper method of finishing an issue is
#       to update it to a closed state.
#       '''
#
#       return self.delete('issues/' + str(issue_ID) + '.xml')

####################################################################################################

class RedmineProject:

    '''Encapsulate a Redmine Project.
    '''

    ##############################################

    def __init__(self, redmine_rest, dom):

        self._redmine_rest = redmine_rest
        self._dom = dom

        self._data = self._redmine_rest.parse_project(dom)
        self.id = self._data['id']

    ##############################################

    def new_issue(self,
                  subject,
                  description='',
                  priority_id=None,
                  tracker_id=None,
                  assigned_to_id=None,
                  user_data=None):
  
        # How to set fixed version ?

        '''Create a new issue for this project.
        '''
  
        if user_data is not None:
            data = user_data.copy()
        else:
            data = {}
  
        data['project_id'] = self.id
        data['subject'] = subject
        data['description'] = description

        # Fixme: use keyargs
        if priority_id is not None:
            data['priority_id'] = priority_id
        if tracker_id is not None:
            data['tracker'] = tracker_id
        if assigned_to_id is not None:
            data['assigned_to_id'] = assigned_to_id
  
        return self._redmine_rest.new_issue_from_dict(data)

####################################################################################################
#
#                                               Test
#
####################################################################################################

if __name__ == '__main__':

    redmine_rest = RedmineRest(url='http://intranet/redmine-it/public',
                               key='02caaf292242bbfde9000291cb9955337fa87518')

    project = redmine_rest.get_project('LaptopControlPanel')

    print redmine_rest.get_issue(173)

    if False:
        project.new_issue(subject='This a test!',
                          description='Just to test REST API.',
                          priority_id=None,
                          tracker_id=None,
                          assigned_to_id=None,
                          user_data=None)

####################################################################################################
#
# End
#
####################################################################################################
