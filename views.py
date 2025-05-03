from django.shortcuts import render, get_object_or_404, redirect,get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProductForm
from .models import Product, Order
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "main/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))

        if quantity > product.quantity:
            return render(request, 'main/product_detail.html', {
                'product': product,
                'error': "Not enough stock available."
            })

        total_price = quantity * product.price
        seller_name = product.seller.username if product.seller else "Unknown Seller"
        order = Order.objects.create(
            buyer=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price,
            seller_name=product.seller.username if product.seller else "UnKnown Seller"
        )

        product.quantity -= quantity
        product.save()

        return redirect('order_confirmation', order_id=order.id)

    return redirect('buyers')

@login_required
def view_orders(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            orders = Order.objects.filter(product__seller=request.user)
            return render(request, 'main/view_orders.html', {'orders': orders, 'role': 'seller'})
        else:
            orders = Order.objects.filter(buyer=request.user)

        return render(request, 'main/view_orders.html', {'orders': orders, 'role': 'buyer'})

    return redirect('login')


@login_required(login_url="login")
def our_farm_view(request):
    return render(request, "main/our_farm.html")

@login_required(login_url="login")
def farmers_view(request):
    return render(request, "main/farmers.html")

@login_required(login_url="login")
def buyers_view(request):
    return render(request, "main/buyers.html")

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            else:
                user = User.objects.create_user(username=username, password=password)
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
    return render(request, 'main/signup.html')

def other_details_view(request):
    if request.method == "POST":
        return redirect('home')
    return render(request, 'main/other_details.html')

def home_view(request):
    return render(request, 'main/home.html')

def farmers_page(request):
    categories = ["Fruits", "Vegetables", "Flowers", "Spices"]
    
    # Ensure products are categorized correctly
    categorized_products = {category: [] for category in categories}
    products = Product.objects.all()

    for product in products:
        category_name = product.category.strip().capitalize()  # Normalize category names
        if category_name in categorized_products:
            categorized_products[category_name].append(product)

   # print("Categorized Products:", categorized_products)
    return render(request, 'main/farmers.html', {
        'categories': categories,
        'categorized_products': categorized_products
    })


def buyers(request, category=None):
    categories = ["Fruits", "Vegetables", "Flowers", "Spices"]
    
    
    if category:
        products = Product.objects.filter(category__iexact=category)  
    else:
        products = Product.objects.all()

    return render(request, 'main/buyers.html', {
        'categories': categories,
        'products': products,
        'selected_category': category
    })
 


def buyers_fruits(request):
    fruits = Product.objects.filter(category='Fruits')
    return render(request, 'main/buyers.html', {'products': fruits, 'category': 'Fruits'})

def buyers_vegetables(request):
    vegetables = Product.objects.filter(category='Vegetables')
    return render(request, 'main/buyers.html', {'products': vegetables, 'category': 'Vegetables'})

def buyers_spices(request):
    spices = Product.objects.filter(category='Spices')
    return render(request, 'main/buyers.html', {'products': spices, 'category': 'Spices'})

def buyers_flowers(request):
    flowers = Product.objects.filter(category='Flowers')
    return render(request, 'main/buyers.html', {'products': flowers, 'category': 'Flowers'})

def quantity_price_view(request):
    if request.method == "POST":
        request.session["quantity"] = request.POST.get("quantity")
        request.session["price"] = request.POST.get("price")
        return redirect("place_order")
    return render(request, 'main/quantity_price.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Product


def place_order_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        if "add_to_cart" in request.POST:
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            return redirect("cart_page")

        elif "confirm_order" in request.POST:
            order = Order.objects.create(
                buyer=request.user,
                product=product,
                quantity=quantity,
                total_price=quantity * product.price,
            )
            return redirect("transaction_page", order_id=order.id)

    return render(request, "main/place_order.html", {"product": product})


def cart_view(request):
    if request.method == "POST":
        if "confirm_order" in request.POST:
            return redirect("order_confirmation")
    return render(request, 'main/cart.html')


def order_confirmation(request, order_id):
    if not order_id:
        return redirect('buyers')

    order = get_object_or_404(Order, id=order_id)
    return render(request, 'main/order_confirmation.html', {'order': order})


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('farmers')
    else:
        form = ProductForm()

    return render(request, 'main/add_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('farmers')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'main/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('farmers')

def product_detail(request, category, product_id):
    
    product = get_object_or_404(Product, id=product_id, category=category)
    
    #print(f"Product: {product.name}, Seller: {product.seller.username}")

    return render(request, 'main/product_detail.html', {
        'product': product, 
        'category': category
})

def category_products(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'main/category_products.html', {'products': products, 'category': category})

def transaction_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        return redirect("order_success")
    return render(request, "main/transaction.html", {"order": order})


def order_confirmation(request):
    return render(request, 'main/order_confirmation.html')


def confirm_order(request, category, product_id):
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        product = get_object_or_404(Product, id=product_id, category=category)
        total_price = product.price * int(quantity)
        return render(request, 'main/order_confirmation.html', {'product': product, 'quantity': quantity, 'total_price': total_price})
    else:
        return redirect('buyers')

def cart_page(request):
    cart = request.session.get("cart", [])
    return render(request, "main/cart.html", {"cart": cart})

def order_success(request):
    return render(request, "main/order_success.html")

def final_order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    product = order.product  # Get the ordered product

    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "Not Selected")
        order.payment_method = payment_method
        if product.quantity >= order.quantity:
            product.quantity -= order.quantity
            product.save()

            order.order_status = "Confirmed"
            order.save()

            messages.success(request, "Your order has been placed successfully!")
            return redirect("order_success")
        else:
            messages.error(request, "Insufficient stock available!")
            return redirect("transaction_page", order_id=order.id)

    return render(request, "main/final_order_confirmation.html", {"order": order})

def home_page(request):
    backgrounds = PageBackground.objects.all()
    return render(request, 'main/home.html', {'backgrounds': backgrounds})