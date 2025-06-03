import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Task, ClickHistory, Product, Reservation , Group , Member
from .forms import TaskForm, ProductForm, ReservationForm, Reservation , GroupForm , MemberForm, UserFilterForm
from django.contrib import messages
from babel.dates import format_date
from .forms import UserForm , UserEditForm
from babel.dates import format_datetime
from django.utils.translation import activate

@login_required
def HomePage(request):
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None  # กำหนด user_profile เป็น None หากไม่มี

    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'web/home.html', context)

@login_required
def HomememPage(request):
    user = request.user
    member_groups = Group.objects.filter(members=user).prefetch_related('members')
    return render(request, 'web/member.html', {'groups': member_groups})

@login_required
def member_detail(request, user_id):
    member = get_object_or_404(User, pk=user_id)
    click_history = ClickHistory.objects.filter(user=member)
    return render(request, 'web/member_detail.html', {
        'member': member,
        'click_history': click_history,
    })

@login_required
def EditProfile(request):
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=user)

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        profile_image = request.FILES.get('profile_image')

        user_profile.address = address
        user_profile.phone = phone
        if profile_image:
            user_profile.profile_image = profile_image
        user_profile.save()

        return redirect('HomePage')

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'web/edit_profile.html', context)

def Register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')

        if email:
            new_user = User.objects.create_user(username=email, email=email, password=password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()

            # สร้าง UserProfile และสัมพันธ์กับ User
            UserProfile.objects.create(user=new_user, phone=phone)

            return redirect('HomePage')

    return render(request, 'web/register.html')

@login_required
def tasking_list(request):
    tasks = Task.objects.all()
    user_completed_tasks = set(ClickHistory.objects.filter(user=request.user, status='success').values_list('task__id', flat=True))
    return render(request, 'web/tasking_list.html', {'tasks': tasks, 'user_completed_tasks': user_completed_tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('tasking_list')
        
@login_required
def proceed_task(request, task_id):
    task = Task.objects.filter(pk=task_id).first()
    if task:
        task.completed = False
        task.save()
        ClickHistory.objects.create(user=request.user, task=task, status='proceed')
    return redirect('tasking_list')

@login_required
def success_task(request, task_id):
    task = Task.objects.filter(pk=task_id).first()
    if task:
        task.completed = True
        task.save()
        ClickHistory.objects.create(user=request.user, task=task, status='success')
    return redirect('tasking_list')

@login_required
def work_report(request):
    form = UserFilterForm(request.GET)
    selected_user_id = request.GET.get('user_id')

    if selected_user_id:
        click_histories = ClickHistory.objects.filter(user_id=selected_user_id)
    else:
        click_histories = ClickHistory.objects.all()

    # แปลงวันที่เป็นภาษาไทยและแสดงปีในรูปแบบ พ.ศ.
    for click_history in click_histories:
        formatted_date = format_datetime(click_history.clicked_date, 'd MMMM yyyy, HH:mm', locale='th_TH')
        # แยกส่วนวันที่
        date_parts = formatted_date.split(' ')
        day = date_parts[0]
        month = date_parts[1]
        year_time = date_parts[2]
        year, time = year_time.split(',')
        # เพิ่ม 543 เพื่อแปลงเป็น พ.ศ.
        year = str(int(year) + 543)
        click_history.clicked_date = f"{day} {month} {year} {time}"

    context = {
        'click_histories': click_histories,
        'form': form,
    }

    return render(request, 'web/work_report.html', context)

@login_required
def user_work_report(request):
    # กรองงานตามผู้ใช้ที่เข้าสู่ระบบ
    user_click_histories = ClickHistory.objects.filter(user=request.user)
    
    # แปลงวันที่เป็นภาษาไทยและเปลี่ยนเป็นปี พ.ศ.
    for click_history in user_click_histories:
        clicked_date = click_history.clicked_date
        # แปลงปี ค.ศ. เป็นปี พ.ศ.
        year_th = clicked_date.year + 543
        # สร้างวันที่ใหม่ด้วยปี พ.ศ.
        clicked_date_th = clicked_date.replace(year=year_th)
        # แปลงวันที่เป็นสตริงในรูปแบบที่ต้องการ
        click_history.clicked_date = format_datetime(clicked_date_th, 'd MMMM yyyy, HH:mm', locale='th_TH')

    context = {
        'click_histories': user_click_histories,
    }
    
    return render(request, 'web/user_work_report.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user  # Set the created_by field to the currently logged-in user
            product.save()
            return redirect('Reserve') 
    else:
        form = ProductForm()
    return render(request, 'web/add_product.html', {'form': form})

def user_products(request):
    user_products = Product.objects.filter(created_by=request.user)
    return render(request, 'web/user_products.html', {'user_products': user_products})

def del_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user == product.created_by:
        product.delete()
    return redirect('Reserve')

def Reserve(request):
    query = request.GET.get('q', '')  # ตั้งค่าเริ่มต้นให้เป็นสตริงว่าง
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'web/reserve.html', {'products': products, 'query': query})


@login_required
def Conreserve(request):
    selected_product_id = request.GET.get('product_id')
    selected_product = get_object_or_404(Product, id=selected_product_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation_date = form.cleaned_data['reserved_date']

            # ตรวจสอบว่ามีการจองสินค้าในวันที่ผู้ใช้ต้องการจะจองหรือไม่
            existing_reservation = Reservation.objects.filter(product=selected_product, reserved_date=reservation_date).exists()
            if existing_reservation:
                return HttpResponseBadRequest("สินค้านี้มีการจองในวันที่เลือกแล้ว")

            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.product = selected_product
            reservation.save()
            return redirect('Reserve')
    else:
        form = ReservationForm()

    # ส่งวันที่ที่ถูกจองไปยังเทมเพลต
    reserved_dates = list(Reservation.objects.filter(product=selected_product).values_list('reserved_date', flat=True))
    reserved_dates_json = json.dumps(reserved_dates, default=str)  # แปลงวันที่ให้เป็น JSON

    return render(request, 'web/conreserve.html', {
        'selected_product': selected_product,
        'form': form,
        'reserved_dates_json': reserved_dates_json  # ส่ง JSON ไปยังเทมเพลต
    })

@login_required
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    for reservation in reservations:
        reserved_date = reservation.reserved_date
        # เพิ่ม 543 ปีเพื่อเปลี่ยนเป็นปี พ.ศ.
        year_th = reserved_date.year + 543
        reserved_date_th = reserved_date.replace(year=year_th)
        formatted_date = format_date(reserved_date_th, format='long', locale='th')
        # แทนที่ 'ค.ศ.' ด้วย 'พ.ศ.'
        formatted_date = formatted_date.replace('ค.ศ.', 'พ.ศ.')
        reservation.formatted_date = formatted_date
    return render(request, 'web/user_reservations.html', {'reservations': reservations})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    messages.success(request, 'การจองถูกยกเลิกเรียบร้อยแล้ว')
    return redirect('user_reservations')

def format_thai_date(date):
    year_th = date.year + 543
    formatted_date = date.replace(year=year_th)
    formatted_date = format_date(formatted_date, format='long', locale='th')
    formatted_date = formatted_date.replace('ค.ศ.', 'พ.ศ.')
    return formatted_date

@login_required
def reservation_list(request):
    reservations = Reservation.objects.all()
    for reservation in reservations:
        reserved_date = reservation.reserved_date
        reservation.formatted_date = format_thai_date(reserved_date)
    context = {
        'reservations': reservations,
    }
    return render(request, 'web/reservation_list.html', context)

def rum_page(request):
    return HttpResponse("This is the rum page.")

@login_required
def reservation_report(request):
    form = UserFilterForm(request.GET or None)
    reservations = Reservation.objects.all()

    if form.is_valid():
        user = form.cleaned_data.get('user_id')
        if user:
            reservations = reservations.filter(user=user)
    
    # แปลงวันที่เป็นภาษาไทยและแสดงปีในรูปแบบ พ.ศ.
    for reservation in reservations:
        # แปลงปี ค.ศ. เป็น พ.ศ.
        formatted_date = format_datetime(reservation.reserved_date, 'd MMMM yyyy', locale='th_TH')
        # แยกส่วนวันที่
        day, month, year = formatted_date.split()
        # เพิ่ม 543 เพื่อแปลงเป็น พ.ศ.
        year = str(int(year) + 543)
        reservation.reserved_date = f"{day} {month} {year}"

    context = {
        'form': form,
        'reservations': reservations,
    }
    return render(request, 'web/reservation_report.html', context)

@login_required
def user_reservation_report(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    
    for reservation in user_reservations:
        reserved_date = reservation.reserved_date
        year_th = reserved_date.year + 543
        reserved_date_th = reserved_date.replace(year=year_th)
        reservation.reserved_date = format_datetime(reserved_date_th, 'd MMMM yyyy', locale='th_TH')
    
    context = {
        'reservations': user_reservations,
    }
    
    return render(request, 'web/user_reservation_report.html', context)

@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'web/group_list.html', {'groups': groups})

@login_required
def group_create(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'web/group_form.html', {'form': form})

@login_required
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    members = Member.objects.filter(group=group)

    if request.method == 'POST':
        if 'save_group' in request.POST:
            form = GroupForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                return redirect('group_update', pk=group.pk)
        elif 'add_member' in request.POST:
            member_form = MemberForm(request.POST, group=group)
            if member_form.is_valid():
                member = member_form.save(commit=False)
                member.group = group
                member.save()
                return redirect('group_update', pk=group.pk)
    else:
        form = GroupForm(instance=group)
        member_form = MemberForm(initial={'group': group}, group=group)

    context = {
        'form': form,
        'member_form': member_form,
        'members': members,
        'group': group,
    }
    return render(request, 'web/group_form.html', context)

@login_required
def make_leader(request, group_pk, member_pk):
    group = get_object_or_404(Group, pk=group_pk)
    member = get_object_or_404(Member, pk=member_pk)

    group.leader = member.user
    group.save()

    return redirect('group_update', group_pk)

@login_required
def remove_member(request, group_pk, member_pk):
    group = get_object_or_404(Group, pk=group_pk)
    member = get_object_or_404(Member, pk=member_pk, group=group)
    member.delete()
    return redirect('group_update', pk=group_pk)

@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        group.delete()
        return redirect('group_list')
    return render(request, 'web/group_confirm_delete.html', {'group': group})

@login_required
def dashboard(request):
    return render(request, 'web/dashboard.html')

@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'web/manage_users.html', {'users': users})

@login_required
def manage_groups(request):
    groups = Group.objects.all()
    return render(request, 'web/manage_groups.html', {'groups': groups})

@login_required
def manage_reservations(request):
    activate('th')
    reservations = Reservation.objects.all()
    for reservation in reservations:
        reserved_date = reservation.reserved_date
        # เพิ่ม 543 ปีเพื่อเปลี่ยนเป็นปี พ.ศ.
        year_th = reserved_date.year + 543
        reserved_date_th = reserved_date.replace(year=year_th)
        formatted_date = format_date(reserved_date_th, format='long', locale='th')
        reservation.formatted_date = formatted_date.replace('ค.ศ.', 'พ.ศ.')
    context = {
        'reservations': reservations,
    }
    return render(request, 'web/manage_reservations.html', context)

@login_required
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'web/manage_products.html', {'products': products})

@login_required
def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserForm()
    return render(request, 'web/user_form.html', {'form': form})

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserForm(instance=user)
    return render(request, 'web/user_form.html', {'form': form})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    return render(request, 'web/user_confirm_delete.html', {'user': user})

@login_required
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_groups')
    else:
        form = GroupForm()
    return render(request, 'web/group_form.html', {'form': form})

@login_required
def group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('manage_groups')
    else:
        form = GroupForm(instance=group)
    return render(request, 'web/group_form.html', {'form': form})

@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('manage_groups')
    return render(request, 'web/group_confirm_delete.html', {'group': group})

@login_required
def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        return redirect('manage_reservations')
    return render(request, 'web/reservation_confirm_delete.html', {'reservation': reservation})

@login_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'web/product_form.html', {'form': form})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'web/product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('manage_products')
    return render(request, 'web/product_confirm_delete.html', {'product': product})

@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'web/manage_users.html', {'users': users})

@login_required
def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserForm()
    return render(request, 'web/user_form.html', {'form': form})

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'web/user_form.html', {'form': form})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    return render(request, 'web/user_confirm_delete.html', {'user': user})