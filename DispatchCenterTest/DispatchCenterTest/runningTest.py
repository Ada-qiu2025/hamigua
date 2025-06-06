# encoding: utf-8

from mypackage.disPacher import *
import time, random
import logging.config, os
import mypackage.comm as cm
import mypackage.stateCenter as sc
import logging.handlers
from multiprocessing import *

doclist=['OSBEL', 'OSBEL_0', 'OSBEL_0_1', 'OSBEL_1', 'WWZwangjie', 'WWZwangjie_0', 'WWZwangjie_0_1', 'WWZwangjie_1', 'WWZwjp', 'WWZwjp_0', 'WWZwjp_0_1', 'WWZwjp_1', 'aihongjing', 'aihongjing_0', 'aihongjing_0_1', 'aihongjing_1', 'aimingjun', 'aimingjun_0', 'aimingjun_0_1', 'aimingjun_1', 'aipeng', 'aipeng_0', 'aipeng_0_1', 'aipeng_1', 'aiyan', 'aiyan_0', 'aiyan_0_1', 'aiyan_1', 'ajx', 'ajx_0', 'ajx_0_1', 'ajx_1', 'anhong', 'anhong_0', 'anhong_0_1', 'anhong_1', 'anli', 'anli_0', 'anli_0_1', 'anli_1', 'anxiao', 'anxiao_0', 'anxiao_0_1', 'anxiao_1', 'anxiujuan', 'anxiujuan_0', 'anxiujuan_0_1', 'anxiujuan_1', 'anxiuli', 'anxiuli_0', 'anxiuli_0_1', 'anxiuli_1', 'anxuejuan', 'anxuejuan_0', 'anxuejuan_0_1', 'anxuejuan_1', 'anyuhua', 'anyuhua3', 'anyuhua3_0', 'anyuhua3_0_1', 'anyuhua3_1', 'anyuhua4', 'anyuhua4_0', 'anyuhua4_0_1', 'anyuhua4_1', 'anyuhua_0', 'anyuhua_0_1', 'anyuhua_1', 'anyuying', 'anyuying_0', 'anyuying_0_1', 'anyuying_1', 'aosong', 'aosong_0', 'aosong_0_1', 'aosong_1', 'aoxiaojin', 'aoxiaojin_0', 'aoxiaojin_0_1', 'aoxiaojin_1', 'baiailian', 'baiailian_0', 'baiailian_0_1', 'baiailian_1', 'baibaoyi', 'baibaoyi_0', 'baibaoyi_0_1', 'baibaoyi_1', 'baichunxia', 'baichunxia_0', 'baichunxia_0_1', 'baichunxia_1', 'baidaopeng', 'baidaopeng_0', 'baidaopeng_0_1', 'baidaopeng_1', 'baidong', 'baidong_0', 'baidong_0_1', 'baidong_1', 'baiguifeng', 'baiguifeng_0', 'baiguifeng_0_1', 'baiguifeng_1', 'baihaiya', 'baihaiya_0', 'baihaiya_0_1', 'baihaiya_1', 'baihongbo', 'baihongbo_0', 'baihongbo_0_1', 'baihongbo_1', 'baijiang', 'baijiang_0', 'baijiang_0_1', 'baijiang_1', 'baijingyi', 'baijingyi_0', 'baijingyi_0_1', 'baijingyi_1', 'bailihong', 'bailihong_0', 'bailihong_0_1', 'bailihong_1', 'bailing', 'bailing_0', 'bailing_0_1', 'bailing_1', 'bailinguo', 'bailinguo_0', 'bailinguo_0_1', 'bailinguo_1', 'baimei', 'baimei_0', 'baimei_0_1', 'baimei_1', 'baimingfang', 'baimingfang_0', 'baimingfang_0_1', 'baimingfang_1', 'baiou', 'baiou_0', 'baiou_0_1', 'baiou_1', 'baiqingling', 'baiqingling_0', 'baiqingling_0_1', 'baiqingling_1', 'bairuijie', 'bairuijie_0', 'bairuijie_0_1', 'bairuijie_1', 'baisaixi', 'baisaixi_0', 'baisaixi_0_1', 'baisaixi_1', 'baishufang', 'baishufang_0', 'baishufang_0_1', 'baishufang_1', 'baixiani', 'baixiani_0', 'baixiani_0_1', 'baixiani_1', 'baixianqun', 'baixianqun_0', 'baixianqun_0_1', 'baixianqun_1', 'baixiaoxue', 'baixiaoxue_0', 'baixiaoxue_0_1', 'baixiaoxue_1', 'baixiaoyan', 'baixiaoyan_0', 'baixiaoyan_0_1', 'baixiaoyan_1', 'baixuepeng', 'baixuepeng_0', 'baixuepeng_0_1', 'baixuepeng_1', 'baixueyan', 'baixueyan_0', 'baixueyan_0_1', 'baixueyan_1', 'baiyu', 'baiyu_0', 'baiyu_0_1', 'baiyu_1', 'baiyuju', 'baiyuju_0', 'baiyuju_0_1', 'baiyuju_1', 'baiyunyiyuan', 'baiyunyiyuan_0', 'baiyunyiyuan_0_1', 'baiyunyiyuan_1', 'baogang', 'baogang_0', 'baogang_0_1', 'baogang_1', 'baoliyang', 'baoliyang_0', 'baoliyang_0_1', 'baoliyang_1', 'baoqingli', 'baoqingli_0', 'baoqingli_0_1', 'baoqingli_1', 'baoqiuping', 'baoqiuping_0', 'baoqiuping_0_1', 'baoqiuping_1', 'baoshihai', 'baoshihai_0', 'baoshihai_0_1', 'baoshihai_1', 'baoyanping', 'baoyanping_0', 'baoyanping_0_1', 'baoyanping_1', 'baoyunan', 'baoyunan_0', 'baoyunan_0_1', 'baoyunan_1', 'bcrjq', 'bcrjq_0', 'bcrjq_0_1', 'bcrjq_1', 'bctct', 'bctct_0', 'bctct_0_1', 'bctct_1', 'bctgsh', 'bctgsh_0', 'bctgsh_0_1', 'bctgsh_1', 'bctjq', 'bctjq_0', 'bctjq_0_1', 'bctjq_1', 'bctlgc', 'bctlgc_0', 'bctlgc_0_1', 'bctlgc_1', 'bctlq', 'bctlq_0', 'bctlq_0_1', 'bctlq_1', 'bctlyq', 'bctlyq_0', 'bctlyq_0_1', 'bctlyq_1', 'bctnxh', 'bctnxh_0', 'bctnxh_0_1', 'bctnxh_1', 'bcttyf', 'bcttyf_0', 'bcttyf_0_1', 'bcttyf_1', 'bctwmy', 'bctwmy_0', 'bctwmy_0_1', 'bctwmy_1', 'bctxgl', 'bctxgl_0', 'bctxgl_0_1', 'bctxgl_1', 'bctxtm', 'bctxtm_0', 'bctxtm_0_1', 'bctxtm_1', 'bctyxm', 'bctyxm_0', 'bctyxm_0_1', 'bctyxm_1', 'bctzhl', 'bctzhl_0', 'bctzhl_0_1', 'bctzhl_1', 'bctzj', 'bctzj_0', 'bctzj_0_1', 'bctzj_1', 'bctzp', 'bctzp_0', 'bctzp_0_1', 'bctzp_1', 'beidongmei', 'beidongmei_0', 'beidongmei_0_1', 'beidongmei_1', 'bekchenyixia', 'bekchenyixia_0', 'bekchenyixia_0_1', 'bekchenyixia_1', 'bekliuyi', 'bekliuyi_0', 'bekliuyi_0_1', 'bekliuyi_1', 'bektfs', 'bektfs_0', 'bektfs_0_1', 'bektfs_1', 'bektr', 'bektr_0', 'bektr_0_1', 'bektr_1', 'bekwjx', 'bekwjx_0', 'bekwjx_0_1', 'bekwjx_1', 'bekzhaobing', 'bekzhaobing_0', 'bekzhaobing_0_1', 'bekzhaobing_1', 'bekzj', 'bekzj_0', 'bekzj_0_1', 'bekzj_1', 'bekzjg', 'bekzjg_0', 'bekzjg_0_1', 'bekzjg_1', 'bianfengyun', 'bianfengyun_0', 'bianfengyun_0_1', 'bianfengyun_1', 'biantaifu', 'biantaifu4', 'biantaifu4_0', 'biantaifu4_0_1', 'biantaifu4_1', 'biantaifu_0', 'biantaifu_0_1', 'biantaifu_1', 'bianzhengwu', 'bianzhengwu_0', 'bianzhengwu_0_1', 'bianzhengwu_1', 'biguoqing', 'biguoqing_0', 'biguoqing_0_1', 'biguoqing_1', 'biminming', 'biminming_0', 'biminming_0_1', 'biminming_1', 'bingqiwei', 'bingqiwei_0', 'bingqiwei_0_1', 'bingqiwei_1', 'binlianqin', 'binlianqin_0', 'binlianqin_0_1', 'binlianqin_1', 'binman', 'binman_0', 'binman_0_1', 'binman_1', 'bisheng', 'bisheng_0', 'bisheng_0_1', 'bisheng_1', 'blwangli', 'blwangli_0', 'blwangli_0_1', 'blwangli_1', 'blwangmin', 'blwangmin_0', 'blwangmin_0_1', 'blwangmin_1', 'blzb', 'blzb_0', 'blzb_0_1', 'blzb_1', 'bolin', 'bolin_0', 'bolin_0_1', 'bolin_1', 'boping', 'boping_0', 'boping_0_1', 'boping_1', 'boxiaoping', 'boxiaoping_0', 'boxiaoping_0_1', 'boxiaoping_1', 'bufangyi', 'bufangyi4', 'bufangyi4_0', 'bufangyi4_0_1', 'bufangyi4_1', 'bufangyi_0', 'bufangyi_0_1', 'bufangyi_1', 'buxiaolan', 'buxiaolan_0', 'buxiaolan_0_1', 'buxiaolan_1', 'buxuejiao', 'buxuejiao_0', 'buxuejiao_0_1', 'buxuejiao_1', 'buzhenrui', 'buzhenrui_0', 'buzhenrui_0_1', 'buzhenrui_1', 'bwklili', 'bwklili_0', 'bwklili_0_1', 'bwklili_1', 'bwkshangjie', 'bwkshangjie_0', 'bwkshangjie_0_1', 'bwkshangjie_1', 'bwkwangyuanlong', 'bwkwangyuanlong_0', 'bwkwangyuanlong_0_1', 'bwkwangyuanlong_1', 'bxhxq', 'bxhxq_0', 'bxhxq_0_1', 'bxhxq_1', 'bxlj', 'bxlj_0', 'bxlj_0_1', 'bxlj_1', 'bxluyan', 'bxluyan_0', 'bxluyan_0_1', 'bxluyan_1', 'bxsongli', 'bxsongli_0', 'bxsongli_0_1', 'bxsongli_1', 'bxy', 'bxy_0', 'bxy_0_1', 'bxy_1', 'bywanghong', 'bywanghong_0', 'bywanghong_0_1', 'bywanghong_1', 'caibangzhen', 'caibangzhen_0', 'caibangzhen_0_1', 'caibangzhen_1', 'caibaochao', 'caibaochao_0', 'caibaochao_0_1', 'caibaochao_1', 'caichengrong', 'caichengrong_0', 'caichengrong_0_1', 'caichengrong_1', 'caichengzhi', 'caichengzhi_0', 'caichengzhi_0_1', 'caichengzhi_1', 'caidan', 'caidan2', 'caidan2_0', 'caidan2_0_1', 'caidan2_1', 'caidan4', 'caidan4_0', 'caidan4_0_1', 'caidan4_1', 'caidan_0', 'caidan_0_1', 'caidan_1', 'caidongchun', 'caidongchun_0', 'caidongchun_0_1', 'caidongchun_1', 'caifei', 'caifei_0', 'caifei_0_1', 'caifei_1', 'caihongmei', 'caihongmei_0', 'caihongmei_0_1', 'caihongmei_1', 'caihongyong', 'caihongyong_0', 'caihongyong_0_1', 'caihongyong_1', 'caila', 'caila_0', 'caila_0_1', 'caila_1', 'caili', 'caili_0', 'caili_0_1', 'caili_1', 'cailiuhong', 'cailiuhong_0', 'cailiuhong_0_1', 'cailiuhong_1', 'caiqihua', 'caiqihua_0', 'caiqihua_0_1', 'caiqihua_1', 'caiqingyong', 'caiqingyong_0', 'caiqingyong_0_1', 'caiqingyong_1', 'cairu', 'cairu_0', 'cairu_0_1', 'cairu_1', 'caishan', 'caishan_0', 'caishan_0_1', 'caishan_1', 'caishijun', 'caishijun_0', 'caishijun_0_1', 'caishijun_1', 'caiwanxiang', 'caiwanxiang_0', 'caiwanxiang_0_1', 'caiwanxiang_1', 'caiwenju', 'caiwenju_0', 'caiwenju_0_1', 'caiwenju_1', 'caixia', 'caixia_0', 'caixia_0_1', 'caixia_1', 'caixiaoli', 'caixiaoli_0', 'caixiaoli_0_1', 'caixiaoli_1', 'caixiaolin', 'caixiaolin_0', 'caixiaolin_0_1', 'caixiaolin_1', 'caiyiling', 'caiyiling_0', 'caiyiling_0_1', 'caiyiling_1', 'caiyunzhai', 'caiyunzhai_0', 'caiyunzhai_0_1', 'caiyunzhai_1', 'caizhaoxia', 'caizhaoxia_0', 'caizhaoxia_0_1', 'caizhaoxia_1', 'caizhikun', 'caizhikun4', 'caizhikun4_0', 'caizhikun4_0_1', 'caizhikun4_1', 'caizhikun_0', 'caizhikun_0_1', 'caizhikun_1', 'caizhongxue', 'caizhongxue_0', 'caizhongxue_0_1', 'caizhongxue_1', 'caizufeng', 'caizufeng_0', 'caizufeng_0_1', 'caizufeng_1', 'caoailing', 'caoailing_0', 'caoailing_0_1', 'caoailing_1', 'caoamei', 'caoamei_0', 'caoamei_0_1', 'caoamei_1', 'caobilan', 'caobilan_0', 'caobilan_0_1', 'caobilan_1', 'caochunyan', 'caochunyan_0', 'caochunyan_0_1', 'caochunyan_1', 'caoguanghua', 'caoguanghua_0', 'caoguanghua_0_1', 'caoguanghua_1', 'caoguangxi', 'caoguangxi_0', 'caoguangxi_0_1', 'caoguangxi_1', 'caoguojing', 'caoguojing_0', 'caoguojing_0_1', 'caoguojing_1', 'caoguoxi', 'caoguoxi_0', 'caoguoxi_0_1', 'caoguoxi_1', 'caohaiyun', 'caohaiyun_0', 'caohaiyun_0_1', 'caohaiyun_1', 'caohongbin', 'caohongbin_0', 'caohongbin_0_1', 'caohongbin_1', 'caohui', 'caohui_0', 'caohui_0_1', 'caohui_1', 'caojiaxi', 'caojiaxi_0', 'caojiaxi_0_1', 'caojiaxi_1', 'caojihong', 'caojihong_0', 'caojihong_0_1', 'caojihong_1', 'caojihua', 'caojihua_0', 'caojihua_0_1', 'caojihua_1', 'caojinquan', 'caojinquan_0', 'caojinquan_0_1', 'caojinquan_1', 'caokai', 'caokai_0', 'caokai_0_1', 'caokai_1', 'caokun', 'caokun_0', 'caokun_0_1', 'caokun_1', 'caolian', 'caolian_0', 'caolian_0_1', 'caolian_1', 'caomenghua', 'caomenghua_0', 'caomenghua_0_1', 'caomenghua_1', 'caomin', 'caomin_0', 'caomin_0_1', 'caomin_1', 'caoming', 'caoming_0', 'caoming_0_1', 'caoming_1', 'caomingyan', 'caomingyan_0', 'caomingyan_0_1', 'caomingyan_1', 'caoning', 'caoning_0', 'caoning_0_1', 'caoning_1', 'caoqiaoli', 'caoqiaoli_0', 'caoqiaoli_0_1', 'caoqiaoli_1', 'caoqing', 'caoqing_0', 'caoqing_0_1', 'caoqing_1', 'caorenchang', 'caorenchang_0', 'caorenchang_0_1', 'caorenchang_1', 'caoshanshan', 'caoshanshan_0', 'caoshanshan_0_1', 'caoshanshan_1', 'caoshenghua', 'caoshenghua_0', 'caoshenghua_0_1', 'caoshenghua_1', 'caoshengli', 'caoshengli_0', 'caoshengli_0_1', 'caoshengli_1', 'caoshengrui', 'caoshengrui2', 'caoshengrui2_0', 'caoshengrui2_0_1', 'caoshengrui2_1', 'caoshengrui_0', 'caoshengrui_0_1', 'caoshengrui_1', 'caoshouzhi', 'caoshouzhi_0', 'caoshouzhi_0_1', 'caoshouzhi_1', 'caoshuyi', 'caoshuyi_0', 'caoshuyi_0_1', 'caoshuyi_1', 'caotao', 'caotao_0', 'caotao_0_1', 'caotao_1', 'caowei', 'caowei2', 'caowei2_0', 'caowei2_0_1', 'caowei2_1', 'caowei3', 'caowei3_0', 'caowei3_0_1', 'caowei3_1', 'caowei_0', 'caowei_0_1', 'caowei_1', 'caoxian', 'caoxian_0', 'caoxian_0_1', 'caoxian_1', 'caoxiaojun', 'caoxiaojun_0', 'caoxiaojun_0_1', 'caoxiaojun_1', 'caoxinwu', 'caoxinwu_0', 'caoxinwu_0_1', 'caoxinwu_1', 'caoxiurong', 'caoxiurong_0', 'caoxiurong_0_1', 'caoxiurong_1', 'caoxueqiu', 'caoxueqiu_0', 'caoxueqiu_0_1', 'caoxueqiu_1', 'caoxueying', 'caoxueying_0', 'caoxueying_0_1', 'caoxueying_1', 'caoyan', 'caoyan_0', 'caoyan_0_1', 'caoyan_1', 'caoyanru', 'caoyanru_0', 'caoyanru_0_1', 'caoyanru_1', 'caoyaoyuan', 'caoyaoyuan_0', 'caoyaoyuan_0_1', 'caoyaoyuan_1', 'caoyoujie', 'caoyoujie2', 'caoyoujie2_0', 'caoyoujie2_0_1', 'caoyoujie2_1', 'caoyoujie_0', 'caoyoujie_0_1', 'caoyoujie_1', 'caoyu', 'caoyu_0', 'caoyu_0_1', 'caoyu_1', 'caoyushan', 'caoyushan_0', 'caoyushan_0_1', 'caoyushan_1', 'caozhen', 'caozhen_0', 'caozhen_0_1', 'caozhen_1', 'cengxiaohua', 'cengxiaohua_0', 'cengxiaohua_0_1', 'cengxiaohua_1', 'cgm', 'cgm_0', 'cgm_0_1', 'cgm_1', 'chaiguran', 'chaiguran_0', 'chaiguran_0_1', 'chaiguran_1', 'chajianjun', 'chajianjun_0', 'chajianjun_0_1', 'chajianjun_1', 'changbinfeng', 'changbinfeng_0', 'changbinfeng_0_1', 'changbinfeng_1', 'changchun', 'changchun3', 'changchun3_0', 'changchun3_0_1', 'changchun3_1', 'changchun4', 'changchun4_0', 'changchun4_0_1', 'changchun4_1', 'changchun_0', 'changchun_0_1', 'changchun_1', 'changhaiying', 'changhaiying_0', 'changhaiying_0_1', 'changhaiying_1', 'changhuiling', 'changhuiling_0', 'changhuiling_0_1', 'changhuiling_1', 'changjianguo', 'changjianguo_0', 'changjianguo_0_1', 'changjianguo_1', 'changjianying', 'changjianying_0', 'changjianying_0_1', 'changjianying_1', 'changqingsong', 'changqingsong_0', 'changqingsong_0_1', 'changqingsong_1', 'changruimiao', 'changruimiao_0', 'changruimiao_0_1', 'changruimiao_1', 'changshenglin', 'changshenglin_0', 'changshenglin_0_1', 'changshenglin_1', 'changxiangrong', 'changxiangrong_0', 'changxiangrong_0_1', 'changxiangrong_1', 'changxuan', 'changxuan_0', 'changxuan_0_1', 'changxuan_1', 'changying', 'changying_0', 'changying_0_1', 'changying_1', 'changyoujun', 'changyoujun_0', 'changyoujun_0_1', 'changyoujun_1', 'chaodingding', 'chaodingding3', 'chaodingding3_0', 'chaodingding3_0_1', 'chaodingding3_1', 'chaodingding4', 'chaodingding4_0', 'chaodingding4_0_1', 'chaodingding4_1', 'chaodingding_0', 'chaodingding_0_1', 'chaodingding_1', 'cheguoxiang', 'cheguoxiang_0', 'cheguoxiang_0_1', 'cheguoxiang_1', 'chejian', 'chejian_0', 'chejian_0_1', 'chejian_1', 'chejiangang', 'chejiangang_0', 'chejiangang_0_1', 'chejiangang_1', 'chemingying', 'chemingying_0', 'chemingying_0_1', 'chemingying_1', 'chenaihong', 'chenaihong_0', 'chenaihong_0_1', 'chenaihong_1', 'chenchang', 'chenchang3', 'chenchang3_0', 'chenchang3_0_1', 'chenchang3_1', 'chenchang4', 'chenchang4_0', 'chenchang4_0_1', 'chenchang4_1', 'chenchang_0', 'chenchang_0_1', 'chenchang_1', 'chenchangcai', 'chenchangcai_0', 'chenchangcai_0_1', 'chenchangcai_1', 'chenchen', 'chenchen_0', 'chenchen_0_1', 'chenchen_1', 'chencheng', 'chencheng_0', 'chencheng_0_1', 'chencheng_1', 'chenchengliang', 'chenchengliang_0', 'chenchengliang_0_1', 'chenchengliang_1', 'chenchuanhu', 'chenchuanhu_0', 'chenchuanhu_0_1', 'chenchuanhu_1', 'chenchunfa', 'chenchunfa_0', 'chenchunfa_0_1', 'chenchunfa_1', 'chenchunmei', 'chenchunmei1', 'chenchunmei1_0', 'chenchunmei1_0_1', 'chenchunmei1_1', 'chenchunmei_0', 'chenchunmei_0_1', 'chenchunmei_1', 'chenchunxiang', 'chenchunxiang_0', 'chenchunxiang_0_1', 'chenchunxiang_1', 'chendada', 'chendada_0', 'chendada_0_1', 'chendada_1', 'chendandan', 'chendandan_0', 'chendandan_0_1', 'chendandan_1', 'chendehua', 'chendehua_0', 'chendehua_0_1', 'chendehua_1', 'chendengfu', 'chendengfu_0', 'chendengfu_0_1', 'chendengfu_1', 'chenderong', 'chenderong_0', 'chenderong_0_1', 'chenderong_1', 'chendong', 'chendong_0', 'chendong_0_1', 'chendong_1', 'chendongmin', 'chendongmin4', 'chendongmin4_0', 'chendongmin4_0_1', 'chendongmin4_1', 'chendongmin_0', 'chendongmin_0_1', 'chendongmin_1', 'chenfei', 'chenfei_0', 'chenfei_0_1', 'chenfei_1', 'chenfeifei', 'chenfeifei_0', 'chenfeifei_0_1', 'chenfeifei_1', 'chenfeng', 'chenfeng_0', 'chenfeng_0_1', 'chenfeng_1', 'chenfengqin', 'chenfengqin_0', 'chenfengqin_0_1', 'chenfengqin_1', 'chenfu', 'chenfu_0', 'chenfu_0_1', 'chenfu_1', 'chenfuying', 'chenfuying_0', 'chenfuying_0_1', 'chenfuying_1', 'chenfuyu', 'chenfuyu_0', 'chenfuyu_0_1', 'chenfuyu_1', 'chengang', 'chengang2', 'chengang2_0', 'chengang2_0_1', 'chengang2_1', 'chengang3', 'chengang3_0', 'chengang3_0_1', 'chengang3_1', 'chengang_0', 'chengang_0_1', 'chengang_1']

isdebug = True
# # logging初始化工作
# logging.basicConfig()
#
# # myapp的初始化工作
# myapp = logging.getLogger('root')
# myapp.setLevel(logging.DEBUG)
#
# # 添加TimedRotatingFileHandler
# # 定义一个1秒换一次log文件的handler
# # 保留3个旧log文件
# filehandler = logging.handlers.TimedRotatingFileHandler("logs/myapp.log", when='S', interval=1, backupCount=3)
# # 设置后缀名称，跟strftime的格式一样
# filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"
# myapp.addHandler(filehandler)


# # # 加载日志的配置文件
logging.config.fileConfig('logging.conf')
logging = logging.getLogger('root')

#定义药师业务数和药师账号为字典类型
busimap = {}

def druggist_doc_busy(doc_name,run_times):
    d = Doctor()
    d.login(doc_name, 2)
    print(doc_name,d.doc_status)
    time.sleep(2)
    busi = 0
    for j in range(run_times):
        if d.doc_status==d.doc_status.DO_MATCH_SUCESS or d.doc_status==d.doc_status.DO_BUSY:
            d.recevice()
            busi+=1
            busimap['doc%s'%doc_name]=busi
            print(busimap)
            time.sleep(2)
            d.endtask()
            d.free()
    return busi

#药师接受随机业务的方差统计
'''pool.apply_async: 这是 multiprocessing.Pool 类中的一个方法，用于在进程池中异步地执行函数。它不会阻塞主程序的执行，而是立即返回一个 AsyncResult 对象，
该对象可以用于获取函数执行的状态和结果非阻塞模线程池返回 是对象 所以做一次回调函数  下段代码的get（）方法就是获取对象的数据'''

'''(pool.apply_async(druggist_doc_busy(),args=(doc_name.__str__(),run_times,)) 代码的作用是将 druggist_doc_busy 函数提交到进程池中异步执行，
并传递两个参数 doc_name.__str__() 和 run_times。返回的 AsyncResult 对象被添加到列表 rs 中，以便后续获取函数的执行结果或检查其状态。'''

def  variance_pool_doc():
    from multiprocessing import Pool
    rs = []
    doc_num = int(input("医生数量:"))
    pool = Pool(processes = int(input("进程池大小:")))
    run_times = int(input("迭代次数:"))
    doc_id=int(input("医生开始的id:"))
    for i in range(doc_num):
        doc_name= doc_id+i
        print("医生账号：%s"%doc_name)
        rs.append(pool.apply_async(druggist_doc_busy(),args=(doc_name.__str__(),run_times,)))
    pool.close()
    pool.join()
    nums = []
    for res in rs:
        nums.append(res.get())  # 拿到所有结果
    print(nums)  # 主进程拿到所有的处理结果,可以在主进程中进行统一进行处理
    #计算方差
    # 简化写法 nums = [res.get() for res in rs]
    # f = statistics.pvariance(nums)
    ex = float(sum(nums)) / len(nums)
    s = 0
    for i in nums:
        s += (i - ex) ** 2
    f = float(s) / len(nums)
    print('-'*30)
    print("方差:{0:2f}".format(f))
    print('-'*30)

# 药店拷机测试,随机做业务
def store_rd_running(mac, sleep_time=1):
    cu = Store()
    while True:
        doc_name = sc.getRdDoc()
        # 先找空闲医生,再找忙碌的医生
        if not doc_name:
            logging.info('药店:%s,开始寻找忙碌的医生' % mac)
            doc_name = sc.getRdDoc(2)

        if doc_name:
            cu.store_login(doc_name, mac,need_strategy=3)
            while True:
                time.sleep(sleep_time)
                is_end = random.randint(0, 10)
                if cu.storestatus in [Storestatus.ST_MATCH_SUCCESS, Storestatus.ST_WAIT, Storestatus.ST_BUSY]:
                    if is_end == 0:
                        cu.endtask()
                    elif is_end == 10:
                        cu.logout()
                elif cu.storestatus == Storestatus.ST_OFFLINE:  # 未登录退出循环
                    break
        else:
            print("no doctor found")
            time.sleep(5)


# 多个药店随机做业务,不停止'''
def mult_store_rd_running(stroe_num):
    from multiprocessing import Process

    for i in range(stroe_num):
        p = Process(target=store_rd_running, args=(i.__str__(),))
        p.start()


# 医生拷机测试,随机做业务
def doc_rd_runing(docname):
    '''单个医生随机做业务'''
    d = Doctor(True)
    if d.login(docname):
        while True:
            workduring = 60  # 每次工作时间为1分钟
            sleeptime = 1  # 每次循环的时间
            leave_time = random.randint(1, 3) * 60  # 每次离开的时间
            leasetime = random.randint(1, 3) * 60  # 每次休息1-5分钟
            work_time = random.randint(10, 30) * 60  # 每次工作10-30分钟
            login_dur = random.randint(2, 5) * 60 * 60  # 每次登陆3-5分钟
            logout_dur = random.randint(10, 15) * 60  # 每次登出,休息3-5分钟

            time.sleep(sleeptime)
            if d.doc_status == Docstatus.DO_MATCH_SUCESS:
                d.recevice(b"101")
            elif d.doc_status == Docstatus.DO_BUSY:  # 检测工作状态
                if (time.time() - d.startwort_time) > workduring:  # 工作时间超过60秒就关闭
                    d.endtask()
            elif d.doc_status == d.doc_status.DO_LEAVE:
                if (time.time() - d.leave_time) > leave_time:  # 离开超过时间就free
                    d.free()
            elif d.doc_status == Docstatus.DO_OFFLINE:
                d.login(docname, 4)

            # 检测暂离的状态
            if ((d.doc_status == 1 or d.doc_status == 2 or d.doc_status == 3 or d.doc_status == 4) and (
                        d.is_Pause == False) and (
                        (time.time() - d.PauseTime) > work_time)):
                d.pause(True)
            elif ((d.doc_status == 1 or d.doc_status == 2 or d.doc_status == 3 or d.doc_status == 4) and (
                        d.is_Pause == True) and (
                        (time.time() - d.PauseTime) > leasetime)):
                d.pause(False)

            if (time.time() - d.loginTime) > login_dur:
                d.logout()
                time.sleep(logout_dur)


# 多个医生拷机测试,随机业务  - 多进程
def multpro_doc_rd():
    '''多个医生随机做业务,不停止'''
    # DocLi = cm.getDocList()
    doc_num = int(input("医生数量:"))
    doc_id = int(input("医生开始ID号:"))
    from multiprocessing import Process

    for i in range(doc_num):
        p = Process(target=doc_rd_runing, args=('doctor_rd_bus:'+str(i+doc_id),))
        p.start()


# 僵尸医生,医生接业务后,不操作.
def doc_always_busy(doc_name):
    d = Doctor()
    d.login(doc_name)

    store = Store()
    store.store_login(doc_name, doc_name)
    time.sleep(2)
    d.recevice()
    time.sleep(999 * 60 * 60)


# 多个僵尸医生
def mult_alays_busy():
    '''多个医生随机做业务,不停止'''
    DocNum = int(input("医生数量:"))
    from multiprocessing import Process
    for i in range(DocNum):
        p = Process(target=doc_always_busy, args=('Doctor_always_busy:'+str(i),))
        p.start()


# 计算单个用户登录调度服务及状态转发的时间
def doc_logintime(doc_name):
    '''计算医生从登录到状态转发到状态中心中间的耗时'''
    d = Doctor()
    d.login(doc_name)
    login_time = sc.find_Doc(doc_name, 0, d.loginTime, 30)
    time.sleep(1)
    d.logout()
    logout_time = sc.find_Doc(doc_name, -1, time.time(), 30)
    return (login_time, logout_time)


# 计算多个用户登录调度服务及状态转发的时间
def mult_doc_logintime():
    from multiprocessing import Pool
    pool_num = int(input("进程池大小:"))
    doc_num = int(input("医生数量:"))
    run_times = int(input("迭代次数:"))

    pool = Pool(processes=pool_num)
    rs = []
    for j in range(run_times):
        for i in range(doc_num):
            rs.append(pool.apply_async(doc_logintime, (str(j) + str(i),)))
    pool.close()
    pool.join()

    # 计算平均值/最大登录时间等信息
    total_login = 0
    total_logout = 0
    max_login_time = 0
    max_logout_time = 0
    for i in rs:
        total_login += i.get()[0]
        total_logout += i.get()[1]
        if i.get()[0] > max_login_time:
            max_login_time = i.get()[0]
        if i.get()[1] > max_logout_time:
            max_logout_time = i.get()[1]

    print('----------------------------------------------------------')
    print('平均登录转发状态时间为:%0.3f' % (total_login / len(rs)))
    print('最大登录时间为:%0.3f' % (max_login_time))
    print('平均登出转发状态时间为:%0.3f' % (total_logout / len(rs)))
    print('最大登出时间为:%0.3f' % (max_logout_time))


# 单个用户排队并计算时间,该测试需要先调用僵尸医生模式.
def store_wait_time_test(mac, sleeptime=0, check_times=100):
    store = Store()
    doc_name = sc.getRdDoc(2)

    if doc_name:
        logging.debug('药店:%s,找到随机医生%s' % (mac, doc_name))
        store.store_login(doc_name, mac)

        logging.debug('药店:%s,开始寻找,药店状态:%s' % (mac, store.storestatus.__str__()))
        start_time = time.time()

        for i in range(check_times):
            if (store.storestatus == store.storestatus.ST_WAIT) or \
                            store.storestatus == store.storestatus.ST_OFFLINE:
                logging.debug('结束寻找,药店:%s,状态:%s,寻找次数:%d' % (mac, store.storestatus.__str__(), i))
                break
            time.sleep(0.1)
            logging.debug('未找到药店:%s,再次发起寻找,药店状态:%s,寻找次数:%d' % (mac, store.storestatus.__str__(), i))
        end_time = time.time()
        time.sleep(sleeptime)
        store.logout()  # 需要调用退出方法,否则会影响进程池下个进程
        return mac, start_time, end_time, end_time - start_time
    else:
        logging.error('没有可用的医生,%s'%mac)


# 多个用户排队时间计算
def mult_store_waittime_test():
    from multiprocessing import Pool
    pool_num = int(input("进程池大小:"))
    store_num = int(input("药店数量:"))
    wait_time = int(input("排队等待时间:"))

    pool = Pool(processes=pool_num)
    rs = []
    # for j in range(run_times):
    for i in range(store_num):
        rs.append(pool.apply_async(store_wait_time_test, (str(i), wait_time)))
    pool.close()
    pool.join()

    # cm.printResult(rs,'药店排队反馈')
    total_time = 0
    max_time = 0
    print('----------------------------------------------------------')
    for i in rs:
        print(i.get())
        total_time += i.get()[3]
        if i.get()[3] > max_time:
            max_time = i.get()[3]
    print('----------------------------------------------------------')
    print('平均排队时间为:%0.3f' % (total_time / len(rs)))
    print('最大排队时间为:%0.3f' % (max_time))
    print('----------------------------------------------------------')


def Running(mac,doclist):
    '''药店请求药师，业务保持，然后退出登录'''
    store=Store()
    time.sleep(2)
    # if (store.storestatus==store.storestatus.ST_OFFLINE):
    store.store_login1(doclist,mac,7)
    time.sleep(2)
    store.endtask()
    store.logout()

def mutiStoreRandomdruggist():
    '''多进程，药店请求随机业务'''
    number = int(input("药店数量:"))
    startdoc=int(input('开始的医生账号：'))
    enddoc=int(input('结束的医生账号：'))
    doclist = "|".join(str(i) for i in range(startdoc,enddoc))
    for d in range(100):
    # while(True):
        for i in range(number):
            mac = 'MAC'+ i.__str__()
            p = Process(target=Running, args=(mac,doclist))
            p.start()

if __name__ == '__main__':
    print('*****************************************************************************************************')
    print('1.医生拷机测试,业务随机    2.药店拷机测试,业务随机    3.持续业务医生   4.测试药店排队时间   5.测试医生登录登出时间   6.药店随机请求药师  7.药师接受随机业务的方差' )
    print('******************************************************************************************************')
    test_type = int(input("请选择测试类型:"))
    if test_type == 1:
        multpro_doc_rd()
    elif test_type == 2:
        stroe_num = int(input("药店数量:"))
        mult_store_rd_running(stroe_num)
    elif test_type == 3:
        mult_alays_busy()
    elif test_type == 4:
        # store_wait_time_test('00')
        print('请先使用3,开启多个忙碌医生.')
        mult_store_waittime_test()
    elif test_type == 5:
        mult_doc_logintime()
    elif test_type == 6:
        mutiStoreRandomdruggist()
    elif test_type ==7:
        print("请先使用6，药店随机请求药师")
        variance_pool_doc()
