from config.cache_conf import get_cache_list_dict,set_cache
from typing import List,Dict,Any

# 新闻相关的缓存方法：新闻分类的读取和写入
# key -- value
CATEGORY_KEY = "news_category"

# 获取新闻分类缓存
async def get_cached_category():
    return await get_cache_list_dict(CATEGORY_KEY)


# 写入新闻分类缓存:缓存的数据，过期时间
# 分类、配置：7200；列表：600；详情：1800;验证码：120 --数据越稳定，缓存越持久
async def set_cached_category(data:List[Dict[str,Any]],expire:int=7200):
    return await set_cache(CATEGORY_KEY,data,expire)


# # 更新新闻分类缓存
# async def update_cached_category(category:List[NewsCategory]):
#     await set_cache(CATEGORY_KEY,category)


# # 删除新闻分类缓存
# async def delete_cached_category():
#     pass
