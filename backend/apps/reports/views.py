from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta

from apps.orders.models import Order
from apps.reservations.models import Reservation
from apps.restaurants.models import Table

class ReportViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def check_permissions(self, request):
        super().check_permissions(request)
        if request.user.role not in ['ADMIN', 'MANAGER']:
            self.permission_denied(request, message="You do not have permission to view reports.")

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today)
        
        today_sales = today_orders.aggregate(total=Sum('total_amount'))['total'] or 0
        completed_orders = today_orders.filter(status=Order.OrderStatus.COMPLETED).count()
        pending_orders = today_orders.filter(status__in=[Order.OrderStatus.PENDING, Order.OrderStatus.CONFIRMED, Order.OrderStatus.PREPARING]).count()
        average_order_value = today_orders.aggregate(avg=Avg('total_amount'))['avg'] or 0
        
        active_reservations = Reservation.objects.filter(reservation_date=today, status=Reservation.ReservationStatus.CONFIRMED).count()
        occupied_tables = Table.objects.filter(status=Table.TableStatus.OCCUPIED).count()
        
        return Response({
            "today_sales": today_sales,
            "today_orders": today_orders.count(),
            "completed_orders": completed_orders,
            "pending_orders": pending_orders,
            "average_order_value": average_order_value,
            "low_stock_items": 0, # Placeholder (No inventory app)
            "active_reservations": active_reservations,
            "occupied_tables": occupied_tables
        })

    @action(detail=False, methods=['get'], url_path='sales/daily')
    def daily_sales(self, request):
        date_str = request.query_params.get('date')
        if date_str:
            target_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            target_date = timezone.now().date()
            
        orders = Order.objects.filter(created_at__date=target_date)
        
        sales = orders.aggregate(
            total_sales=Sum('total_amount'),
            total_tax=Sum('tax_amount'),
            total_discount=Sum('discount_amount')
        )
        
        return Response({
            "date": target_date,
            "orders_count": orders.count(),
            "sales": sales['total_sales'] or 0,
            "tax": sales['total_tax'] or 0,
            "discount": sales['total_discount'] or 0
        })

    @action(detail=False, methods=['get'], url_path='sales/weekly')
    def weekly_sales(self, request):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        
        weekly_data = []
        for i in range(7):
            current_day = start_of_week + timedelta(days=i)
            day_sales = Order.objects.filter(created_at__date=current_day).aggregate(total=Sum('total_amount'))['total'] or 0
            weekly_data.append({
                "date": current_day,
                "day": current_day.strftime("%A"),
                "sales": day_sales
            })
            
        return Response(weekly_data)

    @action(detail=False, methods=['get'], url_path='sales/monthly')
    def monthly_sales(self, request):
        year = request.query_params.get('year', timezone.now().year)
        month = request.query_params.get('month', timezone.now().month)
        
        orders = Order.objects.filter(created_at__year=year, created_at__month=month)
        total_sales = orders.aggregate(total=Sum('total_amount'))['total'] or 0
        
        return Response({
            "year": year,
            "month": month,
            "orders_count": orders.count(),
            "total_sales": total_sales
        })

    @action(detail=False, methods=['get'], url_path='orders')
    def order_analytics(self, request):
        orders = Order.objects.all()
        
        status_counts = orders.values('status').annotate(count=Count('id'))
        total_orders = orders.count()
        average_value = orders.aggregate(avg=Avg('total_amount'))['avg'] or 0
        
        return Response({
            "total_orders": total_orders,
            "average_order_value": average_value,
            "by_status": {item['status']: item['count'] for item in status_counts},
        })

    @action(detail=False, methods=['get'], url_path='menu/popular')
    def popular_menu_items(self, request):
        # Placeholder since no Menu/OrderItem app
        return Response([
            {"menu_item": "Paneer Pizza", "quantity_sold": 152, "revenue": 38000},
            {"menu_item": "Veg Biryani", "quantity_sold": 118, "revenue": 23600},
            {"menu_item": "French Fries", "quantity_sold": 97, "revenue": 14550}
        ])

    @action(detail=False, methods=['get'], url_path='menu/categories')
    def category_sales(self, request):
        # Placeholder since no Menu app
        return Response([
            {"category": "Pizza", "sales": 45000},
            {"category": "Main Course", "sales": 32000},
            {"category": "Beverages", "sales": 18500},
            {"category": "Desserts", "sales": 12300}
        ])

    @action(detail=False, methods=['get'], url_path='inventory')
    def inventory_report(self, request):
        # Placeholder since no Inventory app
        return Response({
            "total_ingredients": 50,
            "low_stock_ingredients": 6,
            "out_of_stock_ingredients": 2,
            "stock_value": 15000,
            "most_consumed": ["Tomato", "Onion", "Cheese"],
            "recent_movements": []
        })

    @action(detail=False, methods=['get'], url_path='reservations')
    def reservation_report(self, request):
        reservations = Reservation.objects.all()
        status_counts = reservations.values('status').annotate(count=Count('id'))
        
        data = {item['status']: item['count'] for item in status_counts}
        total = reservations.count()
        
        cancelled = data.get(Reservation.ReservationStatus.CANCELLED, 0)
        cancellation_rate = (cancelled / total * 100) if total > 0 else 0
        
        return Response({
            "total_reservations": total,
            "by_status": data,
            "cancellation_rate": round(cancellation_rate, 2)
        })

    @action(detail=False, methods=['get'], url_path='tables/occupancy')
    def table_occupancy(self, request):
        tables = Table.objects.all()
        status_counts = tables.values('status').annotate(count=Count('id'))
        
        return Response({
            "total_tables": tables.count(),
            "by_status": {item['status']: item['count'] for item in status_counts}
        })
