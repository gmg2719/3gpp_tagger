from information_extraction.pre_process_data import pre_process_file
from information_extraction.tagging_automater import AutoTagProcessor
from services.document_service import DocumentService
from services.settings_service import SettingService

'''
Environments :
1 - Local
2 - Cloud 

SSL Verify is Boolean to handle the SSL authentication or bypass it.
'''


def download_settings():
    '''
    Download settings of entity JSON for the annotation files to be righly formed.
    :return: N/A
    '''
    # download the project settings for comparision
    setting_service = SettingService(True, 2)
    setting_service.get_project_setting()


def upload_files():
    '''
    Upload generated Files which would the text file and then annotations files to tagtog for further review.
    :return: N/A
    '''
    # Using REST call to upload the data into Server.
    doc_service = DocumentService(True, 2)
    doc_service.push_annotated_verbatim_text(text_file_path, ann_file_path)


if __name__ == '__main__':
    '''
    Pre-process files and tag files based on the rules. 
    '''
    download_settings()
    pre_processed_file = pre_process_file('configs/input_data.txt')
    # Tag the files using the rules set.
    auto_tag_processor = AutoTagProcessor(pre_processed_file, '3ggpp')
    text_file_path, ann_file_path = auto_tag_processor.tag_words()
    upload_files()
