# views.py
from django.shortcuts import render, redirect
from .models import Item, Vendor
from .forms import ItemForm, VendorFormSet

def edit_items(request):
    items = Item.objects.prefetch_related('vendors').all()
    
    if request.method == 'POST':
        for item in items:
            item_form = ItemForm(request.POST, prefix=f'item_{item.id}', instance=item)
            vendor_formset = VendorFormSet(
                request.POST,
                instance=item,
                prefix=f'vendors_{item.id}'
            )
            if item_form.is_valid() and vendor_formset.is_valid():
                print("enter")
                # Save item first
                item = item_form.save()
                
                # Save all vendors first to get IDs for new records
                vendors = vendor_formset.save(commit=False)
                
                # Reset all vendor flags for this item
                Vendor.objects.filter(item=item).update(vendorflag=False)
                
                # Set flag for selected vendor
                selected_vendor_id = request.POST.get(f'vendorflag_{item.id}')
                if selected_vendor_id and selected_vendor_id != 'None':
                    if selected_vendor_id.startswith('new_'):
                        # For new vendors, find the corresponding unsaved instance
                        new_index = int(selected_vendor_id.split('_')[1])
                        if new_index < len(vendors):
                            vendors[new_index].vendorflag = True
                    else:
                        # For existing vendors
                        Vendor.objects.filter(id=selected_vendor_id).update(vendorflag=True)
                
                # Save all vendor instances
                for vendor in vendors:
                    vendor.save()
                
                vendor_formset.save_m2m()
                print("saved")
        
        return redirect('success_view')
    
    # GET request handling remains the same
    forms = []
    for item in items:
        primary_vendor = item.vendors.order_by('-value').first()
        formset = VendorFormSet(prefix=f'vendors_{item.id}', instance=item)
        
        forms.append({
            'item_form': ItemForm(prefix=f'item_{item.id}', instance=item),
            'vendor_formset': formset,
            'item_id': item.id,
            'primary_vendor_id': primary_vendor.id if primary_vendor else None
        })
    
    return render(request, 'test/edit_items.html', {'forms': forms})

def success_view(request):

    """Displays all items with their vendors after update"""
    items = Item.objects.prefetch_related('vendors').all()
    return render(request, 'test/success.html', {'items': items})
