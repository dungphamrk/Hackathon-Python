
import matplotlib.pyplot as plt
import os
import json

products = []

def calculate_status(quantity):
    """Tính trạng thái dựa trên số lượng"""
    if quantity <= 5:
        return "Cần nhập"
    elif quantity > 50:
        return "Khó bán"
    return "Bình thường"

def get_positive_float(prompt):
    """Nhập số thực dương"""
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Giá trị phải lớn hơn 0!")
        except ValueError:
            print("Vui lòng nhập số hợp lệ!")

def get_positive_int(prompt):
    """Nhập số nguyên dương"""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Giá trị phải lớn hơn 0!")
        except ValueError:
            print("Vui lòng nhập số nguyên hợp lệ!")

def find_product(product_id):
    """Tìm sản phẩm theo ID"""
    for product in products:
        if product['id'] == product_id:
            return product
    return None

def display_products():
    """Hiển thị danh sách tất cả sản phẩm"""
    if not products:
        print("Danh sách sản phẩm trống.")
        return
    print(f"{'Mã SP':<10}{'Tên SP':<25}{'Số Lượng':<12}{'Giá Bán':<15}{'Giá Trị Tồn':<15}{'Trạng Thái':<15}")
    print("=" * 102)
    for product in products:
        inventory_value = product.get('inventory_value', product['quantity'] * product['price'])
        status = product.get('status', 'N/A')
        print(f"{product['id']:<10}{product['name']:<25}{product['quantity']:<12}{product['price']:<15,.0f}{inventory_value:<15,.0f}{status:<15}")

def load_data():
    """Đọc dữ liệu sản phẩm từ file data.json"""
    global products
    if products:
        return

    json_path = os.path.join(os.path.dirname(__file__), 'data.json')

    try:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    quantity = int(item.get('quantity', 0))
                    price = float(item.get('price', 0))
                    
                    products.append({
                        'id': str(item.get('id', '')),
                        'name': str(item.get('name', '')),
                        'quantity': quantity,
                        'price': price,
                        'supplier': str(item.get('supplier', '')),
                        'inventory_value': price * quantity,
                        'status': calculate_status(quantity)
                    })
    except Exception as e:
        print(f'Không thể đọc file dữ liệu: {e}')

def clear_screen():
    """Xóa màn hình terminal"""
    os.system('clear')

def add_product():
    """Thêm sản phẩm mới vào danh sách với validation và tự động tính toán"""
    # Nhập và validate Mã SP
    while True:
        product_id = input("Nhập Mã SP: ").strip()
        if not product_id:
            print("Mã SP không được để trống!")
        elif find_product(product_id):
            print("Mã SP đã tồn tại! Vui lòng nhập mã khác.")
        else:
            break
    
    # Nhập Tên SP
    while True:
        product_name = input("Nhập Tên SP: ").strip()
        if product_name:
            break
        print("Tên SP không được để trống!")
    
    # Nhập Giá bán và Số lượng
    price = get_positive_float("Nhập Giá bán: ")
    quantity = get_positive_int("Nhập Số lượng: ")
    
    # Tự động tính toán
    inventory_value = price * quantity
    status = calculate_status(quantity)
    
    products.append({
        'id': product_id,
        'name': product_name,
        'price': price,
        'quantity': quantity,
        'supplier': '',
        'inventory_value': inventory_value,
        'status': status
    })
    
    print(f"\n✓ Sản phẩm đã được thêm thành công!")
    print(f"  Mã SP: {product_id} | Tên: {product_name}")
    print(f"  Giá bán: {price:,.0f} | Số lượng: {quantity}")
    print(f"  Giá trị tồn: {inventory_value:,.0f} | Trạng thái: {status}")

def update_product():
    """Cập nhật thông tin sản phẩm theo ID"""
    product_id = input("Nhập Mã SP cần cập nhật: ").strip()
    product = find_product(product_id)
    
    if not product:
        print(f"✗ Không tìm thấy sản phẩm với Mã SP: {product_id}")
        return
    
    # Hiển thị thông tin hiện tại
    print(f"\nThông tin hiện tại: {product['name']}")
    print(f"  Giá bán: {product['price']:,.0f} | Số lượng: {product['quantity']}")
    print(f"  Giá trị tồn: {product.get('inventory_value', 0):,.0f} | Trạng thái: {product.get('status', 'N/A')}")
    
    # Nhập thông tin mới
    price = get_positive_float("\nNhập Giá bán mới: ")
    quantity = get_positive_int("Nhập Số lượng mới: ")
    
    # Cập nhật
    product['price'] = price
    product['quantity'] = quantity
    product['inventory_value'] = price * quantity
    product['status'] = calculate_status(quantity)
    
    print(f"\n✓ Cập nhật thành công!")
    print(f"  Giá bán: {price:,.0f} | Số lượng: {quantity}")
    print(f"  Giá trị tồn: {product['inventory_value']:,.0f} | Trạng thái: {product['status']}")

def delete_product():
    """Xóa sản phẩm khỏi danh sách theo ID"""
    product_id = input("Nhập Mã SP cần xoá: ").strip()
    
    for i, product in enumerate(products):
        if product['id'] == product_id:
            print(f"\nThông tin sản phẩm: {product['name']}")
            print(f"  Giá bán: {product['price']:,.0f} | Số lượng: {product['quantity']}")
            
            confirm = input("\nBạn có chắc muốn xóa? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                del products[i]
                print("✓ Sản phẩm đã được xoá thành công.")
            else:
                print("✗ Hủy bỏ thao tác xóa.")
            return
    
    print(f"✗ Không tìm thấy sản phẩm với Mã SP: {product_id}")

def search_product():
    """Tìm kiếm sản phẩm theo tên"""
    name = input("Nhập tên sản phẩm cần tìm kiếm: ").strip()
    results = [p for p in products if name.lower() in p['name'].lower()]
    
    if results:
        print(f"\n{'Mã SP':<10}{'Tên SP':<25}{'Số Lượng':<12}{'Giá Bán':<15}{'Trạng Thái':<15}")
        print("=" * 77)
        for p in results:
            print(f"{p['id']:<10}{p['name']:<25}{p['quantity']:<12}{p['price']:<15,.0f}{p.get('status', 'N/A'):<15}")
    else:
        print("Không tìm thấy sản phẩm với tên đã cho.")

def sort_products():
    """Sắp xếp danh sách sản phẩm theo lựa chọn"""
    if not products:
        print("Danh sách sản phẩm trống.")
        return
    
    print("\nChọn cách sắp xếp:")
    print("1. Giá bán tăng dần")
    print("2. Giá trị tồn giảm dần")
    choice = input("Lựa chọn (1-2): ").strip()
    
    if choice == '1':
        products.sort(key=lambda x: x['price'])
        print("Danh sách sản phẩm đã được sắp xếp theo giá bán tăng dần.")
    elif choice == '2':
        products.sort(key=lambda x: x.get('inventory_value', x['price'] * x['quantity']), reverse=True)
        print("Danh sách sản phẩm đã được sắp xếp theo giá trị tồn giảm dần.")
    else:
        print("Lựa chọn không hợp lệ.")

def inventory_statistics():
    """Hiển thị thống kê tổng giá trị và số lượng kho hàng"""
    if not products:
        print("Danh sách sản phẩm trống.")
        return
    
    # Đếm theo trạng thái
    status_count = {"Cần nhập": 0, "Bình thường": 0, "Khó bán": 0}
    for product in products:
        status = product.get('status', 'Bình thường')
        status_count[status] = status_count.get(status, 0) + 1
    
    print("\n" + "="*50)
    print("THỐNG KÊ KHO HÀNG")
    print("="*50)
    print(f"Tổng số sản phẩm: {len(products)}")
    print("-"*50)
    print("Phân loại theo trạng thái:")
    print(f"  - Cần nhập:    {status_count['Cần nhập']} sản phẩm")
    print(f"  - Bình thường: {status_count['Bình thường']} sản phẩm")
    print(f"  - Khó bán:     {status_count['Khó bán']} sản phẩm")
    print("="*50)

def plot_inventory_statistics():
    """Vẽ biểu đồ hình tròn thống kê trạng thái kho hàng"""
    if not products:
        print("Danh sách sản phẩm trống.")
        return
    
    # Đếm theo trạng thái
    status_count = {"Cần nhập": 0, "Bình thường": 0, "Khó bán": 0}
    for product in products:
        status = product.get('status', 'Bình thường')
        status_count[status] = status_count.get(status, 0) + 1
    
    # Lọc các trạng thái có sản phẩm
    statuses = [s for s, c in status_count.items() if c > 0]
    counts = [status_count[s] for s in statuses]
    colors = {'Cần nhập': '#ff6b6b', 'Bình thường': '#4ecdc4', 'Khó bán': '#ffd93d'}
    chart_colors = [colors[s] for s in statuses]
    
    if not statuses:
        print("Không có dữ liệu để vẽ biểu đồ.")
        return
    
    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=90, colors=chart_colors)
    plt.title('Tỷ Lệ Trạng Thái Kho Hàng', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def save_to_json():
    """Lưu dữ liệu sản phẩm vào file data.json"""
    json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        print(f"✓ Dữ liệu đã được lưu vào {json_path}.")
    except Exception as e:
        print(f"✗ Lỗi khi lưu file: {e}")

def main():
    """Hàm chính điều khiển menu chương trình"""
    load_data()  
    while True:
        print("\nMenu Quản Lý Sản Phẩm:")
        print("1. Hiển thị danh sách sản phẩm")
        print("2. Thêm mới sản phẩm")
        print("3. Cập nhật thông tin sản phẩm")
        print("4. Xoá sản phẩm")
        print("5. Tìm kiếm sản phẩm")
        print("6. Sắp xếp danh sách sản phẩm")
        print("7. Thống kê kho hàng")
        print("8. Vẽ biểu đồ thống kê kho hàng")
        print("9. Lưu vào file data.json")
        print("10. Thoát")
        choice = input("Chọn chức năng (1-10): ")
        if choice == '1':
            display_products()
        elif choice == '2':
            add_product()
        elif choice == '3':
            update_product()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            search_product()
        elif choice == '6':
            sort_products()
        elif choice == '7':
            inventory_statistics()
        elif choice == '8':
            plot_inventory_statistics()
        elif choice == '9':
            save_to_json()
        elif choice == '10':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        input("\nNhấn Enter để tiếp tục...")  
        clear_screen()
if __name__ == "__main__":
    main()