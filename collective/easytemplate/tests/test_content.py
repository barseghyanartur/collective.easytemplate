import unittest

from Products.CMFCore.utils import getToolByName

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from AccessControl.User import User

from Products.statusmessages.interfaces import IStatusMessage

from collective.easytemplate.content.TemplatedDocument import ERROR_MESSAGE
from collective.easytemplate.tests.base import EasyTemplateTestCase
class ContentTestCase(EasyTemplateTestCase):
    """ Check that Templated Document functions properly. """
    
    def afterSetUp(self):
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')
    
    def test_create(self):        
        self.loginAsPortalOwner()
        self.portal.invokeFactory("TemplatedDocument", "doc")
        doc = self.portal.doc
        
    def test_render(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory("TemplatedDocument", "doc")
        doc = self.portal.doc
        tests = "Oh joy"
        doc.setCatchErrors(True)
        doc.setTitle(tests)
        doc.setText("${title}")
        output = doc.getTemplatedText()
        messages = IStatusMessage(self.portal.REQUEST).showStatusMessages()        
        
        if messages:
            for m in messages: print str(m.message)
            
        self.assertEqual(len(messages), 0) # No template error messages
        self.assertEqual(str(output), "<p>" + tests + "</p>") # At has automatic HTML wrap

        
    def test_render_failed(self):
        
        self.loginAsPortalOwner()
        self.portal.invokeFactory("TemplatedDocument", "doc")
        doc = self.portal.doc
        doc.setCatchErrors(True)
        doc.setText("#if")
        output = doc.getTemplatedText()
        
        
        messages = IStatusMessage(self.portal.REQUEST).showStatusMessages()        
        self.assertEqual(len(messages), 1) # No template error messages
        self.assertEqual(output, ERROR_MESSAGE)
        
    def test_list_folder(self):
        """ Test our custom template tag, list folder. """
        
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Folder", "folder")
        self.portal.folder.invokeFactory("TemplatedDocument", "doc")
        self.portal.folder.invokeFactory("Document", "doc2")
        doc = self.portal.folder.doc
        doc.setCatchErrors(True)

        doc.setText('$list_folder($folder="folder")')
        print doc.getRawText()                
        output = doc.getTemplatedText()
                
        # Should not happen
        messages = IStatusMessage(self.portal.REQUEST).showStatusMessages()                
        for m in messages: print str(m.message)
        
    
        self.assertEqual(len(messages), 0)
        
        # See that object ids appear in the output (in links)
        output = str(output)
        print output
        self.assertTrue("doc" in output)
        self.assertTrue("doc2" in output)

    
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ContentTestCase))
    return suite