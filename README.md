[![Build Status](https://travis-ci.org/recursively/ContractSpider.svg?branch=master)](https://travis-ci.org/recursively/ContractSpider)

## 运行脚本

```shell
python3.6 ETHspider.py
```
该脚本只支持python3.6以上版本

## 获取合约地址

由于Etherscan.io官网有防爬机制，故采用同步以太坊区块链主链的方式获取合约地址，以太坊主链同步命令：

```shell
geth --rpc --rpcaddr=127.0.0.1 --syncmode=full
```

参数--rpc开启http访问，可通过Web3.HTTPProvider()来获取区块链信息。参数--syncmode设置同步方式，若要获取合约代码，须采用full模式。（以太坊区块链只保存了合约的字节码，若要获取源码，需要调用Etherscan提供的接口）

## 调用接口

代码查询接口为Etherscan.io官方提供的接口：

https://api.etherscan.io/api?module=contract&action=getsourcecode&address=addr&apikey=token

修改address参数和apikey来查询指定合约的代码，apikey可以注册Etherscan账户后获得。如果是非验证合约则无法获取对应代码。

在Etherscan官网上查看API使用情况：
![](http://i38.photobucket.com/albums/e117/bucketuser111/Blog/apistat_zps8p6hde4r.png)

## 设置线程

在main()函数中修改multi_thread_scrape()函数的thread参数可设置线程。

## 发送邮件

添加email_send()函数，爬取完成后自动发送邮件提醒。

## 扫描环境搭建

安装solidity compiler:

```shell
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc
```

安装manticore测试工具：

```shell
sudo pip2 install manticore
```

## 批量扫描代码

运行脚本：

```shell
python3 checkcode.py
```

运行脚本后会在根目录下创建contracts文件夹，里面存放合约代码和代码扫描结果。

## 调用测试工具

```shell
$ manticore ./path/to/contract.sol  # runs, and creates a mcore_* directory with analysis results
```
