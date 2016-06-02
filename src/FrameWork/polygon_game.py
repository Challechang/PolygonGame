#coding:utf-8
import numpy as np
global sum,dp,op,edge,ans,null
def find(start,n):
    global sum, dp, op, edge, ans,null
    if dp[start][n][0]!=null:
        #如果n=1，代表的是自己，返回自己的最大最小值即可
        return (int)(dp[start][n][0]),(int)(dp[start][n][1])
    lmin=[]
    lmax=[]
    #n为顶点数，那么边数为n-1，从边数为i的开始计算
    for i in range(n-1):
        #声明4个变量a,b,c,d
        a,b=find(start,(i+1))
        c,d=find((start+(i+1))%sum,n-(i+1))
        dp[start][i+1][0],dp[start][i+1][1]=a,b
        dp[(start+(i+1))%sum][n-(i+1)][0],dp[(start+(i+1))%sum][n-(i+1)][1]=c,d
        if op[(start+i)%sum]=='+':
            lmin.append(a+c)
            lmax.append(b+d)
        elif op[(start+i)%sum]=='*':
            lmin.append(min(a*c,a*d,b*c,b*d))
            lmax.append(max(a*c,a*d,b*c,b*d))
    edge[start][n][0]=(start+lmin.index(min(lmin)))%sum
    edge[start][n][1]=(start+lmax.index(max(lmax)))%sum
    return min(lmin),max(lmax)

def findpath(start,n,flag):
    global sum, dp, op, edge, ans
    if n!=1:
        #print '删除第',edge[start][n][flag],'条边'#找到最大值要删除的边
        ans.append((int)(edge[start][n][flag]))
        s1=start
        n1=(int)(edge[start][n][flag])-start+1#当前顶点离删除边有多少个顶点            
        if (int)(edge[start][n][flag])<start:
            n1+=sum
        s2=((int)(edge[start][n][flag])+1)%sum
        n2=n-n1
        if op[(int)(edge[start][n][flag])]=='+':            
            findpath(s1,n1,1)
            findpath(s2,n2,1)
        elif op[(int)(edge[start][n][flag])]=='*':
            if (int)(dp[s1][n1][0])*(int)(dp[s2][n2][0])==(int)(dp[start][n][flag]):
                findpath(s1,n1,0)
                findpath(s2,n2,0)
            elif (int)(dp[s1][n1][0])*(int)(dp[s2][n2][1])==(int)(dp[start][n][flag]):
                findpath(s1,n1,0)
                findpath(s2,n2,1)
            elif (int)(dp[s1][n1][1])*(int)(dp[s2][n2][0])==(int)(dp[start][n][flag]):
                findpath(s1,n1,1)
                findpath(s2,n2,0)
            elif (int)(dp[s1][n1][1])*(int)(dp[s2][n2][1])==(int)(dp[start][n][flag]):
                findpath(s1,n1,1)
                findpath(s2,n2,1)


def dealBestPath(lines):
    global sum, dp, op, edge, ans,null
    null='null'*3
    #顶点和边都从0开始编号
    #n=input("输入总顶点数->")
    sum=len(lines)
    #第一维代表的是有n个顶点，第二维代表的是链的长度，范围1-n，第三维的0代表最小值，1代表最大值
    dp=np.array([[[null]*2]*(sum+1)]*sum)#当前链的最大与最小值
    edge=np.array([[[null]*2]*(sum+1)]*sum)#含义是当前链最大与最小值所要删除的边号
    #边的符号
    op=np.array(['']*sum)
    for i in range(sum):
        #每一个顶点，如果这条链只有它自己，那么最大最小都为它自己的顶点值
        dp[i][1][0]=dp[i][1][1]=lines[i].getNode1().getNum()
        op[i]=lines[i].getOpr()

    #递归求解dp[0..n-1][n]
    for i in range(sum):
        dp[i][sum][0],dp[i][sum][1]=find(i,sum)#相当于首先截掉了一条边，除0外op[i-1]，0是op[n-1]

    result=[]
    for j in range(sum):
        result.append((int)(dp[j][sum][1]))
    # print '最优值为->',max(result)
    _index=result.index(max(result))
    ###print _index
    ans=[]
    findpath(_index,sum,1)
    ans.reverse()
    if _index==0:
        #print '删除第',(n-1),'条边'
        ans.insert(0,sum-1)
    else:
        #print '删除第',(_index-1),'条边'
        ans.insert(0,_index-1)
    return ans