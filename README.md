# Peekpa.com

欢迎大家来到皮爷撸码的Peekpa.com源代码。

### 下载源码

使用终端（Terminal），并配合`git clone`命令，可将源码下载到本地：

```shell
$ git clone https://github.com/SwyftG/PeekpaCom.git
```

### 查看文章配对代码

查看此代码的Tag地址：

https://github.com/SwyftG/PeekpaCom/tags

这里面，Tag格式均以`Post_xxx`来命名。`xxx`为文章对应的编号，比如，文章《用Django全栈开发——26. 开发Dashboard功能展示页面》对应的代码，是Tag为`Post_026`下面的代码。

如果你想查看某个标签所指向的文件版本，可以使用 `git checkout` 命令:

```shell
$ git checkout <Tag名称>

### 例如，查看文章《用Django全栈开发——26. 开发Dashboard功能展示页面》对应的代码
$ git checkout Post_026
```

### 环境配置

首先需要Python3，然后使用以下命令安装项目依赖：

```shell
$ pip install -r requirement.txt
```

然后，本地需要安装MySQL服务，并且在`Peekpa/settings.py`文件中，配置`DATABASES`变量信息。

或者自己参考网上资料，更换掉系统的`DATABASES`变量。

### 阿里云线上部署

想要将代码部署到阿里云服务器，可以参考以下两篇文章：

准备服务器（内含购买服务器优惠码）：

- [《用Django全栈开发——28. 部署之准备服务器》](https://mp.weixin.qq.com/s?__biz=MzU3NDgzMTM4OA==&mid=2247484505&idx=1&sn=73b69a065de0662efb9b404f0b0900e8&chksm=fd2d2a2aca5aa33cd74d8bff98619c77eb23fc677e5b7b1f8f87857b13b8b57d0fd451c55542&token=1828688355&lang=zh_CN#rd)


具体的部署操作：

- [《用Django全栈开发——29. 部署之阿里云CentOS+Nginx+uWsgi+Django(上)》](https://mp.weixin.qq.com/s?__biz=MzU3NDgzMTM4OA==&mid=2247484560&idx=1&sn=26d3f0dcff62e89c58bb4ecb0b7e7272&chksm=fd2d2ae3ca5aa3f5117506a54580d3f06942866e79d51cf26cb76eb2f50a8422b9e331797659&token=1828688355&lang=zh_CN#rd)

- [《用Django全栈开发——29. 部署之阿里云CentOS+Nginx+uWsgi+Django(下)》](https://mp.weixin.qq.com/s?__biz=MzU3NDgzMTM4OA==&mid=2247484560&idx=2&sn=952a495a30827c9d581adf3490189592&chksm=fd2d2ae3ca5aa3f5a7134eb55b8ad9b4d850c825b39078e944b68d0bf5dd0efc23b808d304fd&token=1828688355&lang=zh_CN#rd)

### 未完待续。。。

获取更多精彩信息，请关注微信公众号『皮爷撸码』，用代码将生活变得简单。

![](https://raw.githubusercontent.com/SwyftG/PeekpaComPostImage/master/z001/011.png)

