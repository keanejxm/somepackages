#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  resolve_json_data.py
:time  2022/10/17 16:27
:desc  
"""

class ResolveJsonData():
    def __init__(self, data):
        self._data = data

    # 获取解析规则，分解成列表
    @staticmethod
    def _resolve_rules(analyze_rule: str) -> list:
        """
        分析解析json的规则
        @param analyze_rule:
        @return:resolve_rules:list
        """
        resolve_rules = list()
        if analyze_rule:
            if isinstance(analyze_rule, str):
                if analyze_rule.startswith("//"):
                    resolve_rules.append("//")
                analyze_rule = analyze_rule.rstrip("/")
                resolve_res = analyze_rule.lstrip("//").split("/")
                resolve_rules.extend(resolve_res)
                return resolve_rules
            else:
                raise ValueError(f"解析规则必需是【str】类型")
        else:
            raise ValueError(f"解析规则不能为空")

    # 如果是text(),输出数据
    @staticmethod
    def _xpath_text(rjs_list: list):
        """

        @param rjs_list: ResolveJsonData组成的列表
        @return:
        """
        return rjs_list

    # 判断下一步的解析规则是否需要解析出数据，如果可以解析出数据返回True,如果不能返回False
    @staticmethod
    def estimate_next_rule(data, rule_data):
        if rule_data == "text()" and isinstance(data, str):
            return True
        elif rule_data != "text()" and isinstance(data, str):
            return False
        else:
            resp = data.get(rule_data)
            if resp:
                return True
            else:
                return False

    # 当规则以“/”开头
    def _resolve_json_signal(self, rjd_list: list, new_rjd_list: list, resolve_rule: str):
        """
        从json的结构中获取key的值为resolve_rule的值
        @param rjd_list: ResolveJsonData对象组成的列表
        @param new_rjd_list: 将通过规则解析出来的数据组成rjd对象并保存
        @param resolve_rule: 解析规则
        @return:
        """
        for rjd in rjd_list:
            data = rjd._data
            # 如果是数据体是字典
            if isinstance(data, dict):
                for da_key, da_value in data.items():
                    if da_key == resolve_rule:
                        if isinstance(da_value, list):
                            for child_value in da_value:
                                def _judge_type(child_value, new_rjd_list):
                                    if isinstance(child_value, list):
                                        for value in child_value:
                                            _judge_type(value, new_rjd_list)
                                    else:
                                        new_rjd_list.append(ResolveJsonData(child_value))
                                        return new_rjd_list

                                new_rjd_list = _judge_type(child_value, new_rjd_list)
                        else:
                            new_rjd_list.append(ResolveJsonData(da_value))
                    else:
                        if isinstance(da_value, list):
                            for child_value in da_value:
                                def _judge_type(child_value, rjd_list_new):
                                    if isinstance(child_value, list):
                                        for value in child_value:
                                            _judge_type(value, rjd_list_new)
                                    else:
                                        rjd_list_new.append(ResolveJsonData(child_value))
                                    return rjd_list_new

                                rjd_list_new = list()
                                new_rjd = _judge_type(child_value, rjd_list_new)
                                new_rjd_list = self._resolve_json_signal(new_rjd, new_rjd_list, resolve_rule)
                        else:
                            new_rjd = [ResolveJsonData(da_value)]
                            new_rjd_list = self._resolve_json_signal(new_rjd, new_rjd_list, resolve_rule)
            elif isinstance(data, list) or isinstance(data, tuple):
                for new_data in data:
                    new_rjd = [ResolveJsonData(new_data)]
                    new_rjd_list = self._resolve_json_signal(new_rjd, new_rjd_list, resolve_rule)
            else:
                continue
        return new_rjd_list

    def _resolve_json_double(self, rjd_list: list, new_rjd_list: list, resolve_rule: str):
        """"""
        for rjd in rjd_list:
            data = rjd._data
            # 如果是数据体是字典
            if isinstance(data, dict):
                for da_key, da_value in data.items():
                    if da_key == resolve_rule:
                        if isinstance(da_value, list):
                            for child_value in da_value:
                                def _judge_type(child_value, new_rjd_list):
                                    if isinstance(child_value, list):
                                        for value in child_value:
                                            _judge_type(value, new_rjd_list)
                                    else:
                                        new_rjd_list.append(ResolveJsonData(child_value))
                                        return new_rjd_list

                                new_rjd_list = _judge_type(child_value, new_rjd_list)
                        else:
                            new_rjd_list.append(ResolveJsonData(da_value))
                    else:
                        continue
            elif isinstance(data, list) or isinstance(data, tuple):
                for new_data in data:
                    new_rjd = [ResolveJsonData(new_data)]
                    new_rjd_list = self._resolve_json_double(new_rjd, new_rjd_list, resolve_rule)
            else:
                continue
        return new_rjd_list

    def _xpath(self, resolve_rule, rjd_list, new_rjd_list):
        """"""
        # next_rule = resolve_rules[rule_index + 1] if rule_index + 1 < len(resolve_rules) else ""
        if resolve_rule == "//":
            # 从第一个开始遍历
            new_rjd_list = self._resolve_json_double(rjd_list, new_rjd_list, resolve_rule)
            assert new_rjd_list, f"路径{resolve_rule}错误"
            return new_rjd_list
        else:
            new_rjd_list = self._resolve_json_signal(rjd_list, new_rjd_list, resolve_rule)
            assert new_rjd_list, f"路径{resolve_rule}错误"
            return new_rjd_list

    # 解析json
    def xpath(self, analyze_rule):
        rjd_list = [ResolveJsonData(self._data)]
        resolve_rules = self._resolve_rules(analyze_rule)
        for rule_index, resolve_rule in enumerate(resolve_rules):
            new_rjd_list = list()
            if resolve_rule == "text()" and (rule_index + 1) == len(resolve_rules):
                # 说明是解析规则的最后数据，以text()结尾返回解析规则解析出来的文本列表
                for new_rjd in rjd_list:
                    if isinstance(new_rjd._data, str):
                        new_rjd_list.append(new_rjd._data)
                return new_rjd_list
            else:
                new_rjd_list = self._xpath(resolve_rule, rjd_list, new_rjd_list)
                rjd_list = new_rjd_list
        return rjd_list


if __name__ == '__main__':
    json_datass = {'modifytime': 1640843719,
                   'headlines': {
                       'subscribe': [
                           {'id': 'news_jingyao', 'name': '要闻', 'type': 'news', 'fixed': 1, 'parentid': 'group_hot'},
                           {'id': 'news_toutiao', 'name': '推荐', 'type': 'news', 'fixed': 1, 'parentid': 'group_hot'},
                           {'id': 'news_hotlist', 'name': '热榜', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_video', 'name': '视频', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_2019ncov', 'name': '抗疫', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_ent', 'name': '娱乐', 'type': 'news', 'parentid': 'group_ent'},
                           {'id': 'news_youliao', 'name': '有料', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_book', 'name': '免费小说', 'type': 'news', 'parentid': 'group_ent', 'isNew': 1},
                           {'id': 'news_follow', 'name': '关注', 'type': 'news', 'parentid': 'group_hot', 'isNew': 1},
                           {'id': 'local_shijiazhuang', 'name': '石家庄', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_sports', 'name': '体育', 'type': 'news', 'parentid': 'group_sports'},
                           {'id': 'news_finance', 'name': '财经', 'type': 'news', 'parentid': 'group_tech'},
                           {'id': 'news_tech', 'name': '科技', 'type': 'news', 'parentid': 'group_tech'},
                           {'id': 'news_mil', 'name': '军事', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_minivideo', 'name': '小视频', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_inter', 'name': '微天下', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_auto', 'name': '汽车', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_jingyao0704', 'name': '精选', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_5g', 'name': '5G', 'type': 'news', 'parentid': 'group_tech'},
                           {'id': 'news_nba', 'name': 'NBA', 'type': 'news', 'parentid': 'group_sports'},
                           {'id': 'news_funny', 'name': '搞笑', 'type': 'news', 'parentid': 'group_ent'},
                           {'id': 'news_edu', 'name': '教育', 'type': 'news', 'parentid': 'group_life'},
                           {'id': 'news_ast', 'name': '星座', 'type': 'news', 'parentid': 'group_ent'},
                           {'id': 'news_shijiuda', 'name': '新时代', 'type': 'news', 'parentid': 'group_hot'},
                           {'id': 'news_baoxian', 'name': '保险', 'type': 'news', 'parentid': 'group_cul'},
                           {'id': 'news_xinzhi', 'name': '新知', 'type': 'news', 'parentid': 'group_cul'},
                           {'id': 'news_sifa', 'name': '司法', 'type': 'news', 'parentid': 'group_gov'},
                           {'id': 'news_minsheng', 'name': '民生', 'type': 'news', 'parentid': 'group_gov'},
                           {'id': 'news_wolympic', 'name': '冬奥', 'type': 'news', 'parentid': 'group_sports'}
                       ],
                       'groups': [
                           {'title': '热门精选',
                            'id': 'group_hot',
                            'list': [
                                {'id': 'news_toutiao', 'name': '推荐', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_jingyao', 'name': '要闻', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_2019ncov', 'name': '抗疫', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_video', 'name': '视频', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_mil', 'name': '军事', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_shijiuda', 'name': '新时代', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_auto', 'name': '汽车', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_minivideo', 'name': '小视频', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_inter', 'name': '微天下', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'local', 'name': '本地', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_sinawap', 'name': '新浪网', 'type': 'news', 'fixed': 2,
                                 'parentid': 'group_hot'},
                                {'id': 'news_hotlist', 'name': '热榜', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_follow', 'name': '关注', 'type': 'news', 'isNew': 1,
                                 'parentid': 'group_hot'},
                                {'id': 'news_youliao', 'name': '有料', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_jingyao0704', 'name': '精选', 'type': 'news', 'parentid': 'group_hot'},
                                {'id': 'news_school', 'name': '校园', 'type': 'news', 'parentid': 'group_hot'}
                            ]
                            },
                           {'title': '体育竞技',
                            'id': 'group_sports',
                            'list': [{'id': 'news_sports', 'name': '体育', 'type': 'news', 'parentid': 'group_sports'},
                                     {'id': 'news_nba', 'name': 'NBA', 'type': 'news', 'parentid': 'group_sports'},
                                     {'id': 'news_game', 'name': '游戏', 'type': 'news', 'parentid': 'group_sports'},
                                     {'id': 'news_wolympic', 'name': '冬奥', 'type': 'news',
                                      'parentid': 'group_sports'}]},
                           {'title': '轻松娱乐', 'id': 'group_ent',
                            'list': [{'id': 'news_ent', 'name': '娱乐', 'type': 'news', 'parentid': 'group_ent'},
                                     {'id': 'news_ast', 'name': '星座', 'type': 'news', 'parentid': 'group_ent'},
                                     {'id': 'news_funny', 'name': '搞笑', 'type': 'news', 'parentid': 'group_ent'},
                                     {'id': 'news_gossip', 'name': '八卦', 'type': 'news', 'parentid': 'group_ent'},
                                     {'id': 'news_cartoon', 'name': '动漫', 'type': 'news', 'parentid': 'group_ent'},
                                     {'id': 'news_pets', 'name': '宠物', 'type': 'news', 'parentid': 'group_ent'},
                                     {'id': 'news_pic', 'name': '图片', 'type': 'news', 'parentid': 'group_ent'},
                                     {'id': 'news_gif', 'name': 'GIF', 'type': 'news', 'parentid': 'group_ent'},
                                     {'id': 'news_book', 'name': '免费小说', 'type': 'news', 'isNew': 1,
                                      'parentid': 'group_ent'}]},
                           {'title': '科技财经', 'id': 'group_tech',
                            'list': [{'id': 'news_finance', 'name': '财经', 'type': 'news', 'parentid': 'group_tech'},
                                     {'id': 'news_tech', 'name': '科技', 'type': 'news', 'parentid': 'group_tech'},
                                     {'id': 'news_digital', 'name': '数码', 'type': 'news', 'parentid': 'group_tech'},
                                     {'id': 'news_5g', 'name': '5G', 'type': 'news', 'parentid': 'group_tech'},
                                     {'id': 'news_sky', 'name': '航空', 'type': 'news', 'parentid': 'group_tech'},
                                     {'id': 'news_vr', 'name': 'VR', 'type': 'news', 'parentid': 'group_tech'}]},
                           {'title': '生活百态', 'id': 'group_life',
                            'list': [{'id': 'news_edu', 'name': '教育', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'news_eladies', 'name': '女性', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'news_fashion', 'name': '时尚', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'news_health', 'name': '健康', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'news_travel', 'name': '旅游', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'news_home', 'name': '家居', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'news_food', 'name': '美食', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'news_slim', 'name': '健身', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'news_baby', 'name': '育儿', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'house', 'name': '房产', 'type': 'news', 'parentid': 'group_life'},
                                     {'id': 'news_piyao', 'name': '辟谣', 'type': 'news', 'parentid': 'group_life'}]},
                           {'title': '人文艺术', 'id': 'group_cul',
                            'list': [{'id': 'news_blog', 'name': '博客', 'type': 'news', 'parentid': 'group_cul'},
                                     {'id': 'news_xinzhi', 'name': '新知', 'type': 'news', 'parentid': 'group_cul'},
                                     {'id': 'news_baoxian', 'name': '保险', 'type': 'news', 'parentid': 'group_cul'},
                                     {'id': 'news_history', 'name': '历史', 'type': 'news', 'parentid': 'group_cul'},
                                     {'id': 'news_collection', 'name': '收藏', 'type': 'news', 'parentid': 'group_cul'}]},
                           {'title': '政务党建',
                            'id': 'group_gov',
                            'list': [{'id': 'news_tuopin', 'name': '脱贫', 'type': 'news', 'parentid': 'group_gov'},
                                     {'id': 'news_dangjian', 'name': '党建', 'type': 'news', 'parentid': 'group_gov'},
                                     {'id': 'news_zhengwu', 'name': '政务', 'type': 'news', 'parentid': 'group_gov'},
                                     {'id': 'news_zhengfa', 'name': '政法', 'type': 'news', 'parentid': 'group_gov'},
                                     {'id': 'news_sifa', 'name': '司法', 'type': 'news', 'parentid': 'group_gov'},
                                     {'id': 'news_minsheng', 'name': '民生', 'type': 'news', 'parentid': 'group_gov'},
                                     {'id': 'news_jiandang100', 'name': '建党百年', 'type': 'news',
                                      'parentid': 'group_gov'}]}],
                       'recomChannel': [{'id': 'news_pic', 'name': '图片', 'type': 'news', 'parentid': 'group_ent',
                                         'intro': '图说天下资讯直达',
                                         'bgColor': 'D0ECFF'},
                                        {'id': 'news_fashion', 'name': '时尚', 'type': 'news', 'parentid': 'group_life',
                                         'intro': '美容穿搭气场最强', 'bgColor': 'FFF3C8'},
                                        {'id': 'news_eladies', 'name': '女性', 'type': 'news', 'parentid': 'group_life',
                                         'intro': '关爱女性心理生理', 'bgColor': 'E5F7D6'},
                                        {'id': 'news_blog', 'name': '博客', 'type': 'news', 'parentid': 'group_cul',
                                         'intro': '细读人生品味生活',
                                         'bgColor': 'FFE6E6'},
                                        {'id': 'news_health', 'name': '健康', 'type': 'news', 'parentid': 'group_life',
                                         'intro': '养生资讯医疗健康', 'bgColor': 'F6E5FF'},
                                        {'id': 'news_gossip', 'name': '八卦', 'type': 'news', 'parentid': 'group_ent',
                                         'intro': '提供亿点点小八卦', 'bgColor': 'FFE3CC'},
                                        {'id': 'news_travel', 'name': '旅游', 'type': 'news', 'parentid': 'group_life',
                                         'intro': '旅游景点攻略资讯', 'bgColor': 'E4E7FF'},
                                        {'id': 'news_digital', 'name': '数码', 'type': 'news', 'parentid': 'group_tech',
                                         'intro': '数码电器评测解析', 'bgColor': 'FFE4F6'}]},
                   'dChannel': 'news_toutiao',
                   'video': {
                       'list': [{'id': 'video_recom', 'name': '推荐', 'type': 'news'},
                                {'id': 'video_short', 'name': '小视频', 'type': 'news'},
                                {'id': 'video_follow', 'name': '关注', 'type': 'news'},
                                {'id': 'news_live', 'name': '直播', 'type': 'news'},
                                {'id': 'video_movie', 'name': '影视剧', 'type': 'news'},
                                {'id': 'video_funny', 'name': '搞笑', 'type': 'news'},
                                {'id': 'video_ent', 'name': '娱乐', 'type': 'news'},
                                {'id': 'video_minsheng', 'name': '民生', 'type': 'news'},
                                {'id': 'video_mascot', 'name': '萌物', 'type': 'news'},
                                {'id': 'video_music', 'name': '音乐', 'type': 'news'},
                                {'id': 'video_mil', 'name': '军事', 'type': 'news'},
                                {'id': 'video_tech', 'name': '黑科技', 'type': 'news'},
                                {'id': 'video_nba', 'name': 'NBA', 'type': 'news'},
                                {'id': 'video_car', 'name': '汽车', 'type': 'news'},
                                {'id': 'video_delicacy', 'name': '美食', 'type': 'news'}]},
                   'videoFull': {
                       'leftButton': {'id': 'news_live', 'name': '直播', 'type': 'news',
                                      'routeUri': 'sinanews://sina.cn/feed/subfeed.pg?newsId=news_live'},
                       'tabList': [{'id': 'video_follow_full', 'name': '关注', 'type': 'news'},
                                   {'id': 'video_recom_full', 'name': '推荐', 'type': 'news', 'default': 1},
                                   {'id': 'video_short_full', 'name': '探索', 'type': 'news',
                                    'groupId': 'group_video_list',
                                    'list': [
                                        {'id': 'video_short_full', 'name': '探索', 'type': 'news',
                                         'kpic': 'http://n.sinaimg.cn/default/180/w90h90/20210805/4762-fe27294a674460f48dc381189873cb94.png',
                                         'parentid': 'group_video_list'},
                                        {'id': 'video_funny_full', 'name': '搞笑', 'type': 'news',
                                         'kpic': 'http://n.sinaimg.cn/default/180/w90h90/20210805/2182-357240e2aa18f330dd7cf756a2e62931.png',
                                         'parentid': 'group_video_list'},
                                        {'id': 'video_movie_full', 'name': '影视', 'type': 'news',
                                         'kpic': 'http://n.sinaimg.cn/default/180/w90h90/20210805/2371-f7ce0424e43c72234a47122a545772f2.png',
                                         'parentid': 'group_video_list'},
                                        {'id': 'video_ent_full', 'name': '娱乐', 'type': 'news',
                                         'kpic': 'http://n.sinaimg.cn/default/180/w90h90/20210805/22d5-75f205a7edb5e2fbe5fccdd30985ba1e.png',
                                         'parentid': 'group_video_list'},
                                        {'id': 'video_minsheng_full', 'name': '民生', 'type': 'news',
                                         'kpic': 'http://n.sinaimg.cn/default/180/w90h90/20210805/a089-195ea20d03e280a1c7cc9cdc16a638d8.png',
                                         'parentid': 'group_video_list'},
                                        {'id': 'video_mascot_full', 'name': '萌宠', 'type': 'news',
                                         'kpic': 'http://n.sinaimg.cn/default/180/w90h90/20210805/21d2-31d0d7cd5122a93e2681ef1c9570da9b.png',
                                         'parentid': 'group_video_list'},
                                        {'id': 'video_music_full', 'name': '音乐', 'type': 'news',
                                         'kpic': 'http://n.sinaimg.cn/default/180/w90h90/20210805/f1a9-2a68e092ebd4f6ed6a2826a2693a197f.png',
                                         'parentid': 'group_video_list'},
                                        {'id': 'video_mil_full', 'name': '军事', 'type': 'news',
                                         'kpic': 'http://n.sinaimg.cn/default/180/w90h90/20210805/424d-939479ea0f842679a5eed8efe62c4444.png',
                                         'parentid': 'group_video_list'},
                                        {'id': 'video_tech_full', 'name': '黑科技', 'type': 'news',
                                         'kpic': 'http://n.sinaimg.cn/default/180/w90h90/20210805/6da6-64b8a6daaad66adf31285506d823bd6d.png',
                                         'parentid': 'group_video_list'}]}]},
                   'bottomTab': {
                       'list': [{'id': 'news', 'name': '首页', 'type': 'prefab'},
                                {'id': 'video', 'name': '视频', 'type': 'prefab'},
                                {'id': 'desktop', 'name': '直达', 'type': 'prefab'},
                                {'id': 'discovery', 'name': '发现', 'type': 'prefab'},
                                {'id': 'setting', 'name': '我的', 'type': 'prefab'}]}}

    aj = ResolveJsonData(json_datass)
    res = aj.xpath("/groups/list/name")
    for i in res:
        print(i._data)
