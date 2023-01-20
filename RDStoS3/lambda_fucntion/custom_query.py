query = f"""
    with qty as (
    select o.orderNumber, d.quantityOrdered 
    from orders o 
    left join orderdetails d 
    on o.orderNumber=d.orderNumber) 
    
    select orderNumber, sum(quantityOrdered) as totalQTY 
    from qty 
    group by orderNumber
    having totalQTY > 250 order by totalQTY desc"""