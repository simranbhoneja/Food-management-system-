class Query:
    RECENTLY_COMPLETED_ORDERS = """select FoodOrderId,CustomerName,FoodDetails,FoodTotal,OrderDate
                    from FoodOrder fo
                    join Customer c on fo.CustomerId=c.CustomerID
                    where IsComplete=1
                    order by FoodOrderId desc LIMIT 10"""

    PENDING_ORDERS = """select FoodOrderId,CustomerName,FoodDetails,FoodTotal,OrderDate
                    from Customer c 
                    join FoodOrder fo 
                    on c.CustomerId=fo.CustomerId
                    where fo.IsComplete=0 """


    EXECUTE_ORDERS = """Update world.FoodOrder 
                        Set IsComplete=1
                        where FoodOrderId in (%s)"""