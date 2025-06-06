#pragma once

#include <Windows.h>

#ifdef CONSULT_SDK_EXPORTS
#define CONSULT_CLIENT_API  extern "C" __declspec(dllexport)
#else
#define CONSULT_CLIENT_API  extern "C" __declspec(dllimport)
#endif


//医生处理业务的流程
//	ConsultSdkInit(初始化SDK) -->  PharmacistLogin（调用登陆接口并注册事件回调函数)
//                                        |
//                                        |
//										  V			
//	                        callback(int event,  int intVal,  char* strValue, int strLen,  char* jsonVal, int jsonLen, void* pUser)
//                                        |
//										  |	
//										  V
//									收到事件event: 	PE_MATCH_SUCCEED(匹配成功)  用户请求咨询并被服务分配
//                                        |
//                                        |
//                                        V
//                           调用PharmacistReceiveTask接受业务 -->  调用PharmacistCreateUdpConnection建立音视频通道连接
//                                        |
//                                        |
//                                        V
//                                 收到事件event:  PE_UDP_ESTABLISH 通道已建立成功
//                                        |
//                                        |
//                                        V
//									调用CustomStartVideoIntercom 打开音视频采集传输解码 --> 如需录像,继续调用PharmacistRecordStart
//                                    /                             \
//                                   /                               \ 
//                                  V                                 V
//					医生主动结束PharmacistEndTask		      收到事件event:  PE_CLIENT_END_TASK  用户结束业务  (PE_DISCONNECTED与服务断开，PE_CLIENT_OFFLINE用户掉线)
//                                        |                                  |
//                                        |                                  |
//                                        V                                  V
//						调用PharmacistRecordStop（如果开启了录像）-->  PharmacistStopVideoIntercom  -->  PharmacistCloseUdpConnection
//                                        |
//                                        |
//                                        V
//							调用PharmacistFree通知服务自己已准备好接受下一笔业务

//用户回调事件
enum CustomCallbackEvent
{
	CE_MATCH_FAILED,					//匹配失败
	CE_MATCH_SUCCEED,					//匹配成功  
	CE_MATCH_WAIT,						//排队等候中
	CE_DRUGGIST_RECV_TASK,				//医药师已接受任务
	CE_DRUGGIST_END_TASK,				//医药师结束业务
	CE_DRUGGIST_OFFLINE,				//医药师断线
	CE_DRUGGIST_EXCEPTION_END,			//医药师异常断开
	CE_DISCONNECTED,					//与接入服务断开连接
	CE_UDP_ESTABLISH,					//UDP链接建立成功
	CE_PUSH_DRUG,						//推荐药品
	CE_LEAVE,
	CE_SCREENSHOT,						//截图成功回调
	CE_PRESCRIPT_CHECK,					//处方审核结果
};

//医药师回调事件
enum PharmacistCallbackEvent
{
	PE_MATCH_SUCCEED,					//匹配成功	intValue:用户类型 0线下端 1移动端 stringValue:（线下端）药店ID jsonValue:(手机端)手机信息
	PE_AV_CONTROL,						//音视频控制	stringValue:  jsonValue: 控制音视频信息
	PE_FILE_URL,						//图片通知  stringValue:图片url
	PE_GPS_INFO,						//GPS信息   jsonValue:
	PE_CLIENT_END_TASK,					//客户结束业务
	PE_CLIENT_OFFLINE,					//客户掉线
	PE_CLIENT_EXCEPTION_END,			//客户异常断开
	PE_DISCONNECTED,					//与接入服务断开连接
	PE_UDP_ESTABLISH,					//UDP链接建立成功
	PE_LEAVE,
	PE_PUSH_MESSAGE,					//图文消息信息
	PE_WAIT								//排队客户数
};

//消息服务回调事件
enum SMSCallbackEvent
{
	SE_DISCONNECTED,
	SE_SMS,
};


CONSULT_CLIENT_API int ConsultSdkInit();

CONSULT_CLIENT_API int ConsultSdkUnit();

//注册日志回调函数 int-日志级别  const char*-日志数据
CONSULT_CLIENT_API int ConsultSetLogMsgCallback(void (__stdcall *callback)(int, const char*, void*), void* user);


//事件回调void (*callback)(int, int, const char*, const char*, void*)
//参数顺序说明 int 事件ID  int Int型值  const char* 字符串  const char* json字符串 void* 用户自定义指针
//用户API


//用户登录
//need_strategy 分配策略 1随机医生 2随机药师 3指定医生 4指定药师
//need_druggist_id 需要的医生和药师ID need_strategy需要为3或者4
//open_heart 开启内部心跳机制 为false的话需要上层调用心跳接口维护心跳
//server_ip		调度地址
//server_port	调度端口
//name			药店名
//mac			MAC地址
//drugstore_id	药店ID
//hospital_id	医院ID
//only_prescription_checking	请求电子审方

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

//截图初始化

CONSULT_CLIENT_API int CustomInitPhoto(void (__stdcall *callback)(int, int, const char*, const char*, void*), void* user);

CONSULT_CLIENT_API int CustomPhotoStart(HWND view_hwnd, int width, int height, int frame_rate);

CONSULT_CLIENT_API int CustomPhotoStartMinPixel(HWND view_hwnd, int width, int height, int frame_rate);

//截图反初始化
CONSULT_CLIENT_API int CustomPhotoStop();

//截图  传入储存地址
CONSULT_CLIENT_API int CustomPhoto(const char* pic_path);

//发送文件URL
CONSULT_CLIENT_API int CustomSendFileParam(const char* param);


//医药师API
0
//医生药师登陆 
//druggist_type 医生或药师类型 0中药师 1西药师 2执业中药师 3执业西药师 4医生
CONSULT_CLIENT_API int PharmacistLogin(const char* server_ip, int server_port, const char* name, const char* company, const char* druggist_id, int druggist_type, int service_type, void (__stdcall *callback)(int, int, const char*, int, const char*, int, void*), void* user, bool open_heart = true);

CONSULT_CLIENT_API int PharmacistLogout();

//医生接受业务 
//bId 业务ID
CONSULT_CLIENT_API int PharmacistReceiveTask(const char* bId);

//CONSULT_CLIENT_API int PharmacistSetCMSCallback(void (__stdcall *callback)(const char*, const char*, const char*, const char*, const char*, void*), void* user);
CONSULT_CLIENT_API int PharmacistSetCMSCallback(void (__stdcall *callback)(const char*, int, void*), void* user);

//推送药品
CONSULT_CLIENT_API int PharmacistPushDrug(const char* drug_info);

//医生结束业务
//value  结束业务的状态
CONSULT_CLIENT_API int PharmacistEndTask(int value);

//心跳
CONSULT_CLIENT_API int PharmacistHeartbeat();

//发送处方审核结果(电子审方，图片审方)
CONSULT_CLIENT_API int PharmacistPrescriptionCheckResult(const char* str);

//举报用户
CONSULT_CLIENT_API int PharmacistReportUser(const char* user_id);

//通知服务执业者已离开
CONSULT_CLIENT_API int PharmacistToLeave();

//药剂师空闲
CONSULT_CLIENT_API int PharmacistFree();

//建立UDP连接 
CONSULT_CLIENT_API int PharmacistCreateUdpConnection();


//关闭UDP连接
CONSULT_CLIENT_API int PharmacistCloseUdpConnection();

//开启音视频对讲
CONSULT_CLIENT_API int PharmacistStartVideoIntercom(HWND local_hwnd, HWND remote_hwnd, int width, int height, int frame_rate, int video_bitrate, int crop_width, int crop_height, int sample_rate, int channels, int audio_bitrate, int angle, int device_index);

//关闭一视频对讲
CONSULT_CLIENT_API int PharmacistStopVideoIntercom();

//控制本地视频流采集传输 true传输视频流 false关闭视频流传输
CONSULT_CLIENT_API int PharmacistVideoStreamControl(bool open);

//录像接口
//调用前需先开启音视频对讲
CONSULT_CLIENT_API int PharmacistRecordStart(int frame_rate, int video_bitrate, int sample_rate, int channels, int audio_bitrate, \
											 const char* video_file_path, const char* audio_file_path);

//停止录像
CONSULT_CLIENT_API int PharmacistRecordStop();

CONSULT_CLIENT_API int PharmacistAudioRecordStart(const char* audio_file_path, void (__stdcall *callback)(int volume, void* user), void* user);

CONSULT_CLIENT_API int PharmacistAudioRecordStop();

//暂停服务
CONSULT_CLIENT_API int PharmacistPauseService(bool val);

//回叫手机用户
CONSULT_CLIENT_API int PharmacistCallbackPhoneUser(const char* phone_num);



//获取本机摄像头信息
CONSULT_CLIENT_API int GetCameraInfo(void (__stdcall *callback)(int index, const char* name, const char* path, void* user), void* user);




//消息通知API //auth_data: json data 必填uid {"uid":"", ...}
CONSULT_CLIENT_API int SMSLogin(const char* server_ip, int server_port, const char* auth_data, int auth_data_len, void (__stdcall *callback)(int,const char*,int,void*), void* user);

CONSULT_CLIENT_API int SMSLogout();