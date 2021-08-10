// for fetching stock and price data from server
function fetch_() { 
  console.log('runi')
  for (var i = 0; i < $(".item-row").length; i += 1) {

    if (!($.isNumeric($(".item-row").eq(i).find("#rowitemid").val()))){
      $(".item-row").eq(i).find("#rowitemid").val($(".item-row").eq(i).find("#items_name").val())
    }
    var q=$(".item-row").eq(i).find("#rowitemid").val()
    for (p=0;p<$('#product-list').find('option').length;p +=1){
     var opt_val= $("#product-list").find("option").eq(p).val();
     if(q == opt_val){
       $(".item-row").eq(i).find("#items_name").attr({'data-id':q});
        $(".item-row").eq(i).find("#items_name").val($("#product-list").find("option").eq(p).text());
     }
    }
    function fetch_stock(rowitemid,i) {
      $.post(
        "/sale/stock_available/",
        {
          item_name: rowitemid,
        },
        function (data, status) {
          if (data != "None") {
            var data = JSON.parse(data);
            $(".item-row").eq(i).find(".stock").text(data.stock_available);
            $(".item-row").eq(i).find("#price_").val(data.selling_price);
            price_control();
          } else {
            $(".item-row").eq(i).find(".stock").text('0');
            
          }
        }
      );
    }
    fetch_stock(q,i);
  }
}

// for price control and quantity
function price_control() {
  subtotal = 0;
  total_quantity = 0;
  for (var i = 0; i < $(".item-row").length; i += 1) {
    var price_item = $(".item-row").eq(i).find("#price_").val();
    var quantity_item = $(".item-row").eq(i).find("#quantity_").val();
    var p = price_item * quantity_item;
    $(".item-row").eq(i).find("#total_").text(p);
    subtotal += Number($(".item-row").eq(i).find("#total_").text());
    total_quantity += Number($(".item-row").eq(i).find("#quantity_").val());
  }
        $('#price_error_msg').hide()

  $("#subtotal_price").text(subtotal);
  $("#totalQty").text(total_quantity);
  grand_total();
}
// for calculating grandtotal
function grand_total() {
  shipping = Number($("#shipping").val());
  discount = Number($("#discount").val());
  grand_total_val = subtotal + shipping - discount;
  $("#grandTotal").text(grand_total_val);
  returned_cash();
  remaining_amount();
}

// for calculating returned cash
function returned_cash() {
  returned_cash_val =
    Number($("#cash_payment").val()) - Number($("#grandTotal").text());
  $("#returned_cash").text(returned_cash_val);
}

// for remaining amount
function remaining_amount() {
  remaining_amount_val =
    Number($("#grandTotal").text()) - Number($("#paidAmount").val());
  $("#remainingAmount").text(remaining_amount_val);
}

// for create Invoice
function create_invoice(href_,href_post){
  var items = [];
  var total_quantity = 0;
  for (var i = 0; i < $(".item-row").length; i += 1) {
    
    // for checking item name is correct
      if($(".item-row").eq(i).find("#items_name").val()==''){
        $('#items_error_msg').show()
      document.getElementById('items_error_msg').scrollIntoView();
      $(".item-row").eq(i).find("#items_name").focus();
        return false;
    }

    // for checking price value is correct
      if($(".item-row").eq(i).find("#price_").val() == '' || !($.isNumeric($(".item-row").eq(i).find("#price_").val())) ){
        $('#items_error_msg').hide()
        $('#price_error_msg').show()
        document.getElementById('price_error_msg').scrollIntoView();
      $(".item-row").eq(i).find("#price_").focus();
        return false;
}
    var products = {};
    products["item_id"] = $(".item-row").eq(i).find("#items_name").attr('data-id');
    products["item_name"] = $(".item-row").eq(i).find("#items_name").val();
    products["price"] = $(".item-row").eq(i).find("#price_").val();
    products["qty"] = $(".item-row").eq(i).find("#quantity_").val();
    products["total"] = $(".item-row").eq(i).find("#total_").text();
    if ($(".item-row").eq(i).find("#invoice-item").val() != "") {
      items.push(products);
      total_quantity += Number(products["qty"]);
    }
  }

  data = {};
  if($.isNumeric($("#invoice_id").val())){
    data['invoice_id']=$('#invoice_id').val()
  }
  // data['csrfmiddlewaretoken']=$('#csrf').find('input').val();
  if($('#check_customer').val()==1)
  {
    data["customer_name"] = $("#new_customer_id").val();
    data["customer_phone"] = $("#new_customer_phone").val();
  }else{
      data["customerid"] = $('#customer-id').val();
  }
  (data["subtotal"] = $("#subtotal_price").text()),
    (data["discount"] = $("#discount").val()),
    (data["shipping"] = $("#shipping").val()),
    (data["gr_total"] = Number($("#grandTotal").text())),
    (data["totalQty"] = Number($("#totalQty").text())),
    (data["rm_amount"] = Number($("#remainingAmount").text())),
    (data["paid_amount"] = $("#paidAmount").val()),
    (data["cash_payment"] = $("#cash_payment").val()),
    (data["rt_cash"] = Number($("#returned_cash").text())),
    (data["items"] = JSON.stringify(items)),

  $.post(
    href_post,
    data,
    function (data, status) {
    window.location.replace(href_)
    }

    // end post
  );

  // end function
}

function remove_invalid_class(){
    if($("#check_customer").val()==0){
      $('#customer-id').removeClass('is-invalid')
    }else{
      $('#new_customer_id').removeClass('is-invalid')
      $('#new_customer_phone').removeClass('is-invalid')
    };

}

// for update Invoice
function update_invoice() {
  $("#update-invoice").text("Loading...");
  $("#update-invoice-span").addClass("spinner-border spinner-border-sm");
  var items = [];
  var total_quantity = 0;
  for (var i = 0; i < $(".item-row").length; i += 1) {
    var products = {};
    products["item_name"] = $(".item-row").eq(i).find("#items_name").val();
    products["price"] = $(".item-row").eq(i).find("#price_").val();
    products["qty"] = $(".item-row").eq(i).find("#quantity_").val();
    products["total"] = $(".item-row").eq(i).find("#total_").text();
    if ($(".item-row").eq(i).find("#invoice-item").val() != "") {
      items.push(products);
      total_quantity += Number(products["qty"]);
    }
  }
  data = {};
  if ($("#customerid").val() == 0) {
    data["customer_name"] = $("#new_customer_id").val();
    data["customer_phone"] = $("#new_customer_phone").val();
    console.log('work successfully!')

  } else {
    data["customerid"] = $("#customerid").val();
  }
  data["invoice_id"]=$("#invoice_id").val();
  (data["subtotal"] = $("#subtotal_price").text()),
    (data["discount"] = $("#discount").val()),
    (data["shipping"] = $("#shipping").val()),
    (data["gr_total"] = Number($("#grandTotal").text())),
    (data["totalQty"] = Number($("#totalQty").text())),
    (data["rm_amount"] = Number($("#remainingAmount").text())),
    (data["paid_amount"] = $("#paidAmount").val()),
    (data["cash_payment"] = $("#cash_payment").val()),
    (data["rt_cash"] = Number($("#returned_cash").text())),
    (data["items"] = JSON.stringify(items)),
    console.log("work3");
  $.post(
    "/sale/update/invoice/",
    data,
    function (data, status) {
      $("#update-invoice").text("Create Invoice");
      $("#update-invoice-span").removeClass("spinner-border spinner-border-sm");
      window.location.replace('/sale/');
    }

    // end post
  );

  // end function
}

$(document).ready(function () {

  price_control();
  
  $('#existing_customer').hide()
  $("#add_new_customer").click(function () {    
    $("#check_customer").val('1');
    $("#customer-id").val('');
    $("#customer-id").hide();
  $("#new_customer_div").append('<input type="text" onkeypress="remove_invalid_class()" class="form-control" id="new_customer_id" placeholder="Enter Customer Name" required ><br><input type="text" onkeypress="remove_invalid_class()" autocomplete="off" class="form-control" name="customer_phone" id="new_customer_phone" minlenght="9"  pattern="[0-9]*" placeholder="Enter Phone" required>');
  $('#existing_customer').show().text("Existing Customer")
  $('#add_new_customer').hide()
  
});

$("#existing_customer").click(function () {
  $('#customer-id').removeClass('is-invalid')
    $("#check_customer").val('0');
  $('#existing_customer').text("").hide();
  $("#new_customer_div").empty();
  $("#customer-id").show();
  $('#add_new_customer').show()
  });

  $("#addRow").click(function () {
    $("#hiderow").before(
      '<tr class="item-row"><td id="item-name" autocomplete="off" class="item-name"><input data-id="" autofocus onfocusout="fetch_()" onselect="fetch_()" id="items_name" class="custom-select"  list="product-list" placeholder="item" type="text"></td><td class="stock">0</td><td><input id="price_" onkeyup="price_control()"  class="form-control" placeholder="Price" type="number" > </td><td><input class="form-control" size="1" id ="quantity_" placeholder="Quantity" onkeyup="price_control()" value="1" type="text"></td><td><span id="total_" class="total">0.00</span></td><td style="display: none;"><input type="hidden" id="rowitemid"></td></tr>'
    );
  });

  $("#deleteRow").click(function () {
    $("#item_table").find(".item-row").last().remove();
    price_control();
  });
  
  $(".submit-invoice").click(function () {
    var orignol_text=$(this).text()
    console.log(orignol_text)
    $(this).text('Loading...')
    href_=$(this).attr('href')
    href_post=$('#add_sale_href_post').val()
    if($(".item-row").length==0)
    {
      $('#items_error_msg').show()
      document.getElementById('items_error_msg').scrollIntoView();
      $(this).text(orignol_text)
      return false;
    }
    
    else if($('#check_customer').val()==1)
    {
      if(!(document.getElementById('new_customer_id').checkValidity())){
        $('#new_customer_id').addClass('is-invalid')
        $('#new_customer_id').focus()
      $(this).text(orignol_text)
        return false;

      }
      else if(!(document.getElementById('new_customer_phone').checkValidity())){
          $('#new_customer_phone').addClass('is-invalid')
        $('#new_customer_phone').focus()
      $(this).text(orignol_text)

        return false;
      }
      else{
      create_invoice(href_,href_post);
    }
    }
    else
    {
      if($('#customer-id').val()==''){
        $('#customer-id').addClass('is-invalid');
        $('#customer-id').focus();
      $(this).text(orignol_text)

        return false;
      }
      else{
      create_invoice(href_,href_post);
      }
    }
    
    // end create_invoice
  });

  $("#update-invoice").click(function () {
    console.log()
    href_post=$('#update_sale_href_post').val()
    href_=$(this).attr('href')
    create_invoice(href_,href_post);
    // end create_invoice
  });

  $("#discount").keyup(function () {
    grand_total();
  });

$('#customer-id').change(function(){
  $('#customer-id').removeClass('is-invalid')
});

  $("#shipping").keyup(function () {
    grand_total();
  });

  $("#cash_payment").keyup(function () {
    returned_cash();
  });

  $("#paidAmount").keyup(function () {
    remaining_amount();
  });

  // end
});