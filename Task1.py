
# coding: utf-8

# In[13]:


import pandas as pd

def Data_Format(orders, orderLines):
    
    data_all = orders.set_index('OrderID').join(orderLines.set_index('OrderId')).reset_index()
    data_all.columns = ['OrderID', 'DateTime', 'CustomerID', 'ProductId', 'Price']

    table1 = data_all.groupby('ProductId').count().sort_values('Price', ascending=False).reset_index()
    table1 = table1[['ProductId', 'OrderID']].rename(index=str, columns={'OrderID': 'Count'}) # Количество товаров

    table2 = data_all.groupby('ProductId').sum().reset_index() 
    table2 = table2[['ProductId', 'Price']].rename(index=str, columns={'Price': 'Sum_price'}) # Общаая сумма товаров

    table3 = data_all.groupby('OrderID').sum().reset_index()
    table3 = table3.rename(index=str, columns={'OrderID': 'OrderId'})
    table3 = table3[['OrderId', 'Price']].rename(index=str, columns={'Price': 'Sum_order'})
    table3 = data_all.set_index('OrderID').join(table3.set_index('OrderId'))
    table3 = table3.groupby('ProductId').mean().reset_index()
    table3  = table3[['ProductId', 'Sum_order']].rename(index=str, columns={'Sum_order': 'Average_order_price'}) # Cредний чек для каждоо товара

    table_final = table1.set_index('ProductId').join(table2.set_index('ProductId')).reset_index()
    table_final = table_final.set_index('ProductId').join(table3.set_index('ProductId')).reset_index()

    return table_final

# Тест1

orders = pd.DataFrame(columns=['DateTime', 'CustomerID', 'OrderID'])
orderLines = pd.DataFrame(columns=['OrderId', 'ProductId', 'Price'])

orders['DateTime'] = [20190604, 20190604, 20190604, 20190605, 20190605, 20190605, 20190606, 20190607]
orders['CustomerID'] = [1, 1, 2, 2, 2, 2, 3, 4]
orders['OrderID'] = [1, 2, 3, 4, 5, 6, 7, 8]
orderLines['OrderId'] = [1, 1, 2, 3, 4, 4, 5, 6, 7, 8]
orderLines['ProductId'] = [2, 1, 1, 4, 2, 5, 1, 6, 7, 8]
orderLines['Price'] = [200, 300, 300, 350, 210, 245, 305, 900, 1000, 1500]


correct_data = pd.DataFrame(columns=['ProductId', 'Count', 'Sum_price', 'Average_order_price'])

correct_data['ProductId'] = [1, 2, 4, 5, 6, 7, 8]
correct_data['Count'] = [3, 2, 1, 1, 1, 1, 1]
correct_data['Sum_price'] = [905, 410, 350, 245, 900, 1000, 1500]
correct_data['Average_order_price'] = [368.33, 477.5, 350, 455, 900, 1000, 1500]

data = Data_Format(orders, orderLines)
data['Average_order_price'] = [round(x, 2) for x in data['Average_order_price']]


from pandas.util.testing import assert_frame_equal
try:
    assert_frame_equal(data, correct_data)
    print("Ответ верный. Тест успешно пройден")
except:
    print("Ответ не верный")

