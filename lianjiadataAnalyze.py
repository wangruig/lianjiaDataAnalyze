import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 指定画布风格
plt.style.use("fivethirtyeight")

# Mac环境下设置中文字体
# plt.rcParams['font.family'] = ['Arial Unicode MS'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
# sns.set_style({'font.sans-serif':['Arial Unicode MS','Arial']})

# Windows环境下设置中文字体
sns.set_style({'font.sans-serif':['simhei','Arial']})
house_df = pd.read_excel(r'house.xlsx')
# 看一下数据长什么样子
# print(house_df.head())
# print(house_df.info())
house_df.dropna(inplace=True)
house_df['houseTotalMoney'] = house_df['houseTotalMoney'].apply(lambda x: float(x.replace('万', '')))
house_df['houseSinglePrice'] = house_df['houseSinglePrice'].apply(lambda x: float(x.replace('元/平米', '')))
house_df['houseDownPayment'] = house_df['houseDownPayment'].apply(lambda x: float(x.replace('万', '')))
house_df['houseBuildingArea'] = house_df['houseBuildingArea'].apply(lambda x: float(x.replace('㎡', '')))
house_df['totalFloor'] = house_df['houseFloor'].apply(lambda x:re.search('\d+', x).group())

house_df['Region'] = house_df['houseLocation'].apply(lambda x:x.split('/')[0])

# 按区域分析数量和价格
df_house_count = house_df.groupby('Region')['houseId'].count().sort_values(ascending=False).to_frame().reset_index().reindex(['Region', 'Count'], axis=1)
df_house_mean = house_df.groupby('Region')['houseSinglePrice'].mean().sort_values(ascending=False).to_frame().reset_index()

f, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(12, 18))
sns.barplot(x='Region', y='houseSinglePrice', palette='Blues_d', data=df_house_mean, ax=ax1)
ax1.set_title('成都各区二手房每平米单价对比')
ax1.set_xlabel('区域')
ax1.set_ylabel('每平米单价')

sns.barplot(x='Region', y='Count', palette='Greens_d', data=df_house_count, ax=ax2)
ax2.set_title('成都各区二手房数量对比')
ax2.set_xlabel('区域')
ax2.set_ylabel('数量')

sns.boxplot(x='Region', y='houseTotalMoney', data=house_df, ax=ax3)
ax3.set_title('成都各区二手房房屋总价')
ax3.set_xlabel('区域')
ax3.set_ylabel('房屋总价')
plt.savefig(r'image/img1')
plt.show()
f, [ax1,ax2] = plt.subplots(1, 2, figsize=(16, 6))
# 房屋面积
sns.distplot(house_df['houseBuildingArea'], ax=ax1, color='r')
sns.kdeplot(house_df['houseBuildingArea'], shade=True, ax=ax1)
ax1.set_xlabel('面积')

# 房屋面积和价格的关系
sns.regplot(x='houseBuildingArea', y='houseTotalMoney', data=house_df, ax=ax2)
ax2.set_xlabel('面积')
ax2.set_ylabel('总价')

plt.savefig('image/img2')
plt.show()
# 户型情况
f, ax1 = plt.subplots(figsize=(12,12))
sns.countplot(y='houseType', data=house_df, ax=ax1)
ax1.set_title('房屋户型', fontsize=15)
ax1.set_xlabel('数量')
ax1.set_ylabel('户型')
plt.savefig('image/img3')
plt.show()
#装修情况
f, [ax1,ax2,ax3] = plt.subplots(1, 3, figsize=(20, 5))
sns.countplot(house_df['houseDecoration'], ax=ax1)
sns.barplot(x='houseDecoration', y='houseTotalMoney', data=house_df, ax=ax2)
sns.boxplot(x='houseDecoration', y='houseTotalMoney', data=house_df, ax=ax3)

plt.savefig('image/img4')
plt.show()
