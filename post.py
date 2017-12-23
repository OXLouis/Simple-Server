
def insert(comment,dir,url):
    keyword = """<div class="main-content1">
        <h2>发表评论</h2>  <!--使用h2标签实现标题样式-->
        <form action="http://192.168.155.1:8000"""+url+"""" method="post">
            <table border="1" cellpadding=10 cellspacing=0 width=400>
                <tr>
                    <td>评论：</td>
                    <td><input type="text" name="comment" /></td>
                </tr>
                <tr>
                    <th colspan="2">
                        <input type="reset" value="清除数据" />
                        <input type="submit" value="提交数据" />
                    </th>
                </tr>
            </table>
        </form>
    </div>"""
    str1 = """
    <div class="main-content1">
            <h3> 评论:</h3>"""
    str2 = """
    </div>"""
    if comment.find('<') !=-1 or comment.find('>') != -1:
        comment = '非法信息已经被屏蔽'
    file = open(dir,'r',encoding='UTF-8')
    content = file.read()
    post = content.find(keyword)
    if post != -1:
        content = content[:post+len(keyword)]+str1+comment+str2+content[post+len(keyword):]
        file = open(dir,'w',encoding='UTF-8')
        file.write(content)
    file.close()