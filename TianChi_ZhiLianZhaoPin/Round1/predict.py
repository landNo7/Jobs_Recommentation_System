import pandas as pd
import joblib as jl
from functools import partial
import difflib
import numpy as np


def string_similar(s,s1, s2):
    return difflib.SequenceMatcher(None, s[s1], s2).quick_ratio()

# def pred(live_city_id,desire_jd_city_id,desire_jd_industry_id,desire_jd_type_id,desire_jd_salary_id,cur_industry_id,
#          cur_jd_type,cur_salary_id,cur_degree_id,birthday,start_work_date,experience):
def pred(s='-,-其他化妆师400106000房地产/建筑/建材/工程后期制作0500107000本科242015调色员|彩妆|护肤'):
    allUser = pd.read_csv('D:\\WorkFile\\TianChi_ZhiLianZhaoPin\\round1_train\\table1_user.csv')
    allUser = allUser.astype(str)
    allUser['tem123'] = [''.join(i) for i in allUser.values]
    # s2=live_city_id+desire_jd_city_id+desire_jd_industry_id+desire_jd_type_id+desire_jd_salary_id+cur_industry_id+cur_jd_type+cur_salary_id+cur_degree_id+birthday+start_work_date+experience
    # s2='-,-其他化妆师400106000房地产/建筑/建材/工程后期制作0500107000本科242015调色员|彩妆|护肤'
    allUser['ratio']=allUser.apply(partial(string_similar, s1='tem123', s2=s), axis=1).sort_values()
    similar_user=allUser.sort_values('ratio', ascending=False)[['user_id', 'ratio']].reset_index()
    # print df.apply(partial(apply_sm, c1='A', c2='B'), axis=1)
    clf=jl.load('D:\\WorkFile\\TianChi_ZhiLianZhaoPin\\model\\satisfied.pkl')
    all_data = pd.read_csv('D:\\WorkFile\\TianChi_ZhiLianZhaoPin\\Round1\\alldata.csv')
    test_user = all_data[all_data['user_id']==similar_user.loc[0,'user_id']]
    # test_user = pd.DataFrame({'user_id':similar_user.loc[similar_user[0],'user_id'],'live_city_id':live_city_id,'desire_jd_city_id':desire_jd_city_id,
    #                           'desire_jd_industry_id':desire_jd_industry_id,'desire_jd_type_id':desire_jd_type_id,'desire_jd_salary_id':desire_jd_salary_id,
    #                           'cur_industry_id':cur_industry_id,'cur_jd_type':cur_jd_type,'cur_salary_id':cur_salary_id,'cur_degree_id':cur_degree_id,
    #                           'birthday':birthday,'start_work_date':start_work_date,'experience':experience})
    # test_user['desire_jd_city_id'] = test_user['desire_jd_city_id'].apply(lambda x: re.findall('\d+', x))
    # test_user['desire_jd_salary_id'] = test_user['desire_jd_salary_id'].astype(str)
    # test_user['min_desire_salary'] = test_user['desire_jd_salary_id'].apply(get_min_salary)
    # test_user['max_desire_salary'] = test_user['desire_jd_salary_id'].apply(get_max_salary)
    # test_user['min_cur_salary'] = test_user['cur_salary_id'].apply(get_min_salary)
    # test_user['max_cur_salary'] = test_user['cur_salary_id'].apply(get_max_salary)
    # test_user.drop(['desire_jd_salary_id', 'cur_salary_id'], axis=1, inplace=True)
    #
    # test_action = pd.read_csv('D:\\WorkFile\\TianChi_ZhiLianZhaoPin\\round1_train\\table3_action.csv')
    # test_action = test_action[test_action['user_id']==similar_user.loc[similar_user[0]]][['user_id', 'jd_no']]
    # print(test)
    # test = pd.read_csv(test_data_path + 'zhaopin_round1_user_exposure_B_20190819', sep=' ')
    # test_action['user_jd_cnt'] = test_action.groupby(['user_id', 'jd_no'])['jd_no'].transform('count').values
    # test_action['jd_cnt'] = test_action.groupby(['user_id'])['jd_no'].transform('count').values
    # test_action['jd_nunique'] = test_action.groupby(['user_id'])['jd_no'].transform('nunique').values
    # test_action = test_action.drop_duplicates()
    #
    # test_user['delivered'] = -1
    # test_user['satisfied'] = -1
    #
    # test = test_action.merge(test_user, on='user_id', how='left')
    # test = test.merge(train_jd, on='jd_no', how='left')

    print('test data base feats already generated ...')

    use_feats = [c for c in test_user.columns if c not in ['user_id', 'jd_no', 'delivered', 'satisfied'] +
                 ['desire_jd_industry_id', 'desire_jd_type_id', 'cur_industry_id', 'cur_jd_type', 'experience',
                  'jd_title', 'jd_sub_type', 'job_description\n']]
    test_user['satisfied'] = clf.predict(test_user[use_feats], num_iteration=clf.best_iteration)
    print(clf.best_score['valid_0']['auc'])
    return test_user.sort_values('satisfied', ascending=False)[['jd_title','city','jd_sub_type','require_nums','max_salary','min_salary','is_travel','min_work_year','max_work_year','user_work_year','min_edu_level_num','satisfied']].reset_index()

if __name__ == "__main__":
    print('program test beginning')
    user_jd=pred()
    print(user_jd)
    # min_work_year = {103: 1, 305: 3, 510: 5, 1099: 10}
    # max_work_year = {103: 3, 305: 5, 510: 10}
    # degree_map = {'其他': 0, '初中': 1, '中技': 2, '中专': 2, '高中': 2, '大专': 3, '本科': 4,
    #               '硕士': 5, 'MBA': 5, 'EMBA': 5, '博士': 6}
    #
    #
    # train_data_path = 'D:\\WorkFile\\TianChi_ZhiLianZhaoPin\\round1_train\\'
    # train_user = pd.read_csv(train_data_path + 'table1_user.csv')
    # print(train_user.loc[:, 'desire_jd_city_id'])
    # print(train_user['desire_jd_city_id'])