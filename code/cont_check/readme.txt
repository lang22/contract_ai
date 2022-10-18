系统ES跟本地ES更换时注意的点

1. app/json_models 中的parse_json方法
2. cont_check/ES_check_api.py 中的两个方法get_fullText_by_ES   get_sims_by_ES
3. config 数据库连接，数据库密码不一致，修改成你自己的