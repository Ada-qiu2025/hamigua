#pragma once

#include <Windows.h>

#ifdef CONSULT_SDK_EXPORTS
#define CONSULT_CLIENT_API  extern "C" __declspec(dllexport)
#else
#define CONSULT_CLIENT_API  extern "C" __declspec(dllimport)
#endif


//ҽ������ҵ�������
//	ConsultSdkInit(��ʼ��SDK) -->  PharmacistLogin�����õ�½�ӿڲ�ע���¼��ص�����)
//                                        |
//                                        |
//										  V			
//	                        callback(int event,  int intVal,  char* strValue, int strLen,  char* jsonVal, int jsonLen, void* pUser)
//                                        |
//										  |	
//										  V
//									�յ��¼�event: 	PE_MATCH_SUCCEED(ƥ��ɹ�)  �û�������ѯ�����������
//                                        |
//                                        |
//                                        V
//                           ����PharmacistReceiveTask����ҵ�� -->  ����PharmacistCreateUdpConnection��������Ƶͨ������
//                                        |
//                                        |
//                                        V
//                                 �յ��¼�event:  PE_UDP_ESTABLISH ͨ���ѽ����ɹ�
//                                        |
//                                        |
//                                        V
//									����CustomStartVideoIntercom ������Ƶ�ɼ�������� --> ����¼��,��������PharmacistRecordStart
//                                    /                             \
//                                   /                               \ 
//                                  V                                 V
//					ҽ����������PharmacistEndTask		      �յ��¼�event:  PE_CLIENT_END_TASK  �û�����ҵ��  (PE_DISCONNECTED�����Ͽ���PE_CLIENT_OFFLINE�û�����)
//                                        |                                  |
//                                        |                                  |
//                                        V                                  V
//						����PharmacistRecordStop�����������¼��-->  PharmacistStopVideoIntercom  -->  PharmacistCloseUdpConnection
//                                        |
//                                        |
//                                        V
//							����PharmacistFree֪ͨ�����Լ���׼���ý�����һ��ҵ��

//�û��ص��¼�
enum CustomCallbackEvent
{
	CE_MATCH_FAILED,					//ƥ��ʧ��
	CE_MATCH_SUCCEED,					//ƥ��ɹ�  
	CE_MATCH_WAIT,						//�ŶӵȺ���
	CE_DRUGGIST_RECV_TASK,				//ҽҩʦ�ѽ�������
	CE_DRUGGIST_END_TASK,				//ҽҩʦ����ҵ��
	CE_DRUGGIST_OFFLINE,				//ҽҩʦ����
	CE_DRUGGIST_EXCEPTION_END,			//ҽҩʦ�쳣�Ͽ�
	CE_DISCONNECTED,					//��������Ͽ�����
	CE_UDP_ESTABLISH,					//UDP���ӽ����ɹ�
	CE_PUSH_DRUG,						//�Ƽ�ҩƷ
	CE_LEAVE,
	CE_SCREENSHOT,						//��ͼ�ɹ��ص�
	CE_PRESCRIPT_CHECK,					//������˽��
};

//ҽҩʦ�ص��¼�
enum PharmacistCallbackEvent
{
	PE_MATCH_SUCCEED,					//ƥ��ɹ�	intValue:�û����� 0���¶� 1�ƶ��� stringValue:�����¶ˣ�ҩ��ID jsonValue:(�ֻ���)�ֻ���Ϣ
	PE_AV_CONTROL,						//����Ƶ����	stringValue:  jsonValue: ��������Ƶ��Ϣ
	PE_FILE_URL,						//ͼƬ֪ͨ  stringValue:ͼƬurl
	PE_GPS_INFO,						//GPS��Ϣ   jsonValue:
	PE_CLIENT_END_TASK,					//�ͻ�����ҵ��
	PE_CLIENT_OFFLINE,					//�ͻ�����
	PE_CLIENT_EXCEPTION_END,			//�ͻ��쳣�Ͽ�
	PE_DISCONNECTED,					//��������Ͽ�����
	PE_UDP_ESTABLISH,					//UDP���ӽ����ɹ�
	PE_LEAVE,
	PE_PUSH_MESSAGE,					//ͼ����Ϣ��Ϣ
	PE_WAIT								//�Ŷӿͻ���
};

//��Ϣ����ص��¼�
enum SMSCallbackEvent
{
	SE_DISCONNECTED,
	SE_SMS,
};


CONSULT_CLIENT_API int ConsultSdkInit();

CONSULT_CLIENT_API int ConsultSdkUnit();

//ע����־�ص����� int-��־����  const char*-��־����
CONSULT_CLIENT_API int ConsultSetLogMsgCallback(void (__stdcall *callback)(int, const char*, void*), void* user);


//�¼��ص�void (*callback)(int, int, const char*, const char*, void*)
//����˳��˵�� int �¼�ID  int Int��ֵ  const char* �ַ���  const char* json�ַ��� void* �û��Զ���ָ��
//�û�API


//�û���¼
//need_strategy ������� 1���ҽ�� 2���ҩʦ 3ָ��ҽ�� 4ָ��ҩʦ
//need_druggist_id ��Ҫ��ҽ����ҩʦID need_strategy��ҪΪ3����4
//open_heart �����ڲ��������� Ϊfalse�Ļ���Ҫ�ϲ���������ӿ�ά������
//server_ip		���ȵ�ַ
//server_port	���ȶ˿�
//name			ҩ����
//mac			MAC��ַ
//drugstore_id	ҩ��ID
//hospital_id	ҽԺID
//only_prescription_checking	���������

CONSULT_CLIENT_API int CustomLogin(const char* server_ip, int server_port, const char* name, const char* mac, const char* drugstore_id, 
	int need_strategy, const char* need_druggist_id, int hospital_id, int only_prescription_checking, int busi_id, const char* json_str, const char* device_type, 
	void (__stdcall *callback)(int, int, const char*, const char*, void*), void* user, bool open_heart = true);

CONSULT_CLIENT_API int CustomLogout();

CONSULT_CLIENT_API int CustomEndTask();

CONSULT_CLIENT_API int CustomHeartbeat();

CONSULT_CLIENT_API int CustomCreateUdpConnection();

CONSULT_CLIENT_API int CustomCloseUdpConnection();

CONSULT_CLIENT_API int CustomStartVideoIntercom(HWND local_hwnd, HWND remote_hwnd, int width, int height, int frame_rate, int video_bitrate, int crop_width, int crop_height, int sample_rate, int channels, int audio_bitrate);

CONSULT_CLIENT_API int CustomStopVideoIntercom();

//��ͼ��ʼ��

CONSULT_CLIENT_API int CustomInitPhoto(void (__stdcall *callback)(int, int, const char*, const char*, void*), void* user);

CONSULT_CLIENT_API int CustomPhotoStart(HWND view_hwnd, int width, int height, int frame_rate);

CONSULT_CLIENT_API int CustomPhotoStartMinPixel(HWND view_hwnd, int width, int height, int frame_rate);

//��ͼ����ʼ��
CONSULT_CLIENT_API int CustomPhotoStop();

//��ͼ  ���봢���ַ
CONSULT_CLIENT_API int CustomPhoto(const char* pic_path);

//�����ļ�URL
CONSULT_CLIENT_API int CustomSendFileParam(const char* param);


//ҽҩʦAPI
0
//ҽ��ҩʦ��½ 
//druggist_type ҽ����ҩʦ���� 0��ҩʦ 1��ҩʦ 2ִҵ��ҩʦ 3ִҵ��ҩʦ 4ҽ��
CONSULT_CLIENT_API int PharmacistLogin(const char* server_ip, int server_port, const char* name, const char* company, const char* druggist_id, int druggist_type, int service_type, void (__stdcall *callback)(int, int, const char*, int, const char*, int, void*), void* user, bool open_heart = true);

CONSULT_CLIENT_API int PharmacistLogout();

//ҽ������ҵ�� 
//bId ҵ��ID
CONSULT_CLIENT_API int PharmacistReceiveTask(const char* bId);

//CONSULT_CLIENT_API int PharmacistSetCMSCallback(void (__stdcall *callback)(const char*, const char*, const char*, const char*, const char*, void*), void* user);
CONSULT_CLIENT_API int PharmacistSetCMSCallback(void (__stdcall *callback)(const char*, int, void*), void* user);

//����ҩƷ
CONSULT_CLIENT_API int PharmacistPushDrug(const char* drug_info);

//ҽ������ҵ��
//value  ����ҵ���״̬
CONSULT_CLIENT_API int PharmacistEndTask(int value);

//����
CONSULT_CLIENT_API int PharmacistHeartbeat();

//���ʹ�����˽��(�����󷽣�ͼƬ��)
CONSULT_CLIENT_API int PharmacistPrescriptionCheckResult(const char* str);

//�ٱ��û�
CONSULT_CLIENT_API int PharmacistReportUser(const char* user_id);

//֪ͨ����ִҵ�����뿪
CONSULT_CLIENT_API int PharmacistToLeave();

//ҩ��ʦ����
CONSULT_CLIENT_API int PharmacistFree();

//����UDP���� 
CONSULT_CLIENT_API int PharmacistCreateUdpConnection();


//�ر�UDP����
CONSULT_CLIENT_API int PharmacistCloseUdpConnection();

//��������Ƶ�Խ�
CONSULT_CLIENT_API int PharmacistStartVideoIntercom(HWND local_hwnd, HWND remote_hwnd, int width, int height, int frame_rate, int video_bitrate, int crop_width, int crop_height, int sample_rate, int channels, int audio_bitrate, int angle, int device_index);

//�ر�һ��Ƶ�Խ�
CONSULT_CLIENT_API int PharmacistStopVideoIntercom();

//���Ʊ�����Ƶ���ɼ����� true������Ƶ�� false�ر���Ƶ������
CONSULT_CLIENT_API int PharmacistVideoStreamControl(bool open);

//¼��ӿ�
//����ǰ���ȿ�������Ƶ�Խ�
CONSULT_CLIENT_API int PharmacistRecordStart(int frame_rate, int video_bitrate, int sample_rate, int channels, int audio_bitrate, \
											 const char* video_file_path, const char* audio_file_path);

//ֹͣ¼��
CONSULT_CLIENT_API int PharmacistRecordStop();

CONSULT_CLIENT_API int PharmacistAudioRecordStart(const char* audio_file_path, void (__stdcall *callback)(int volume, void* user), void* user);

CONSULT_CLIENT_API int PharmacistAudioRecordStop();

//��ͣ����
CONSULT_CLIENT_API int PharmacistPauseService(bool val);

//�ؽ��ֻ��û�
CONSULT_CLIENT_API int PharmacistCallbackPhoneUser(const char* phone_num);



//��ȡ��������ͷ��Ϣ
CONSULT_CLIENT_API int GetCameraInfo(void (__stdcall *callback)(int index, const char* name, const char* path, void* user), void* user);




//��Ϣ֪ͨAPI //auth_data: json data ����uid {"uid":"", ...}
CONSULT_CLIENT_API int SMSLogin(const char* server_ip, int server_port, const char* auth_data, int auth_data_len, void (__stdcall *callback)(int,const char*,int,void*), void* user);

CONSULT_CLIENT_API int SMSLogout();