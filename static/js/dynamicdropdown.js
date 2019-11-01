function dynamicdropdown(listindex)
{
    document.getElementById("secondcategory").length = 0;
    switch (listindex)
    {
    case "men" :
        if($('#clothingcategory').length != 0){
            document.getElementById('clothingcategory').remove()
        }
        document.getElementById("secondcategory").options[0]=new Option("Select Men's Category","");
        document.getElementById("secondcategory").options[1]=new Option("Clothing","Clothing");
        document.getElementById("secondcategory").options[2]=new Option("Shoes","Shoes");
        document.getElementById("secondcategory").options[3]=new Option("Watches","Watches");
        break;

    case "women" :
        if($('#clothingcategory').length != 0){
            document.getElementById('clothingcategory').remove()
        }
        document.getElementById("secondcategory").options[0]=new Option("Select Women's Category","");
        document.getElementById("secondcategory").options[1]=new Option("pigs","pigs");
        document.getElementById("secondcategory").options[2]=new Option("chicken","chicken");
        break;

    default:
        if($('#clothingcategory').length != 0){
            document.getElementById('clothingcategory').remove()
        }
        document.getElementById("secondcategory").options[0]=new Option("No Category","");
        break;
    }
    return true;
}

function dynamicdropdown1(listindex)
{
    document.getElementById("thirdcategory").length = 0;
    switch (listindex)
    {
    case "Clothing" :
        $("#dynamicdropdowntag").append('<select class="form-control ml-3" id="clothingcategory"><option value="">No Category</option></select>')
        document.getElementById("thirdcategory").options[0]=new Option("No Clothing Category","");
        document.getElementById("thirdcategory").options[1]=new Option("Shirt","Shirt");
        document.getElementById("thirdcategory").options[2]=new Option("Hoodies & Sweatshirts","Hoodies & Sweatshirts");
        document.getElementById("thirdcategory").options[3]=new Option("Sweaters","Sweaters");
        document.getElementById("thirdcategory").options[4]=new Option("Jacket & Coats","Jacket & Coats");
        document.getElementById("thirdcategory").options[5]=new Option("Jeans","chicJeansken");
        document.getElementById("thirdcategory").options[6]=new Option("Pants","Pants");
        document.getElementById("thirdcategory").options[7]=new Option("Shorts","Shorts");
        document.getElementById("thirdcategory").options[8]=new Option("Active","Active");
        document.getElementById("thirdcategory").options[9]=new Option("Swim","Swim");
        document.getElementById("thirdcategory").options[10]=new Option("Suits & Sport Coats","Suits & Sport Coats");
        document.getElementById("thirdcategory").options[11]=new Option("Underwear","Underwear");
        document.getElementById("thirdcategory").options[12]=new Option("Socks","Socks");
        document.getElementById("thirdcategory").options[13]=new Option("Sleep & Lounge","Sleep & Lounge");
        document.getElementById("thirdcategory").options[14]=new Option("T-Shirts & Tanks","T-Shirts & Tanks");
        break;

    case "Shoes" :
        if($('#clothingcategory').length != 0){
            document.getElementById('clothingcategory').remove()
        }
        document.getElementById("thirdcategory").options[0]=new Option("No Shoes Category","");
        document.getElementById("thirdcategory").options[1]=new Option("Adidas","Adidas");
        document.getElementById("thirdcategory").options[2]=new Option("Crocs","Crocs");
        document.getElementById("thirdcategory").options[3]=new Option("Converse","Converse");
        document.getElementById("thirdcategory").options[4]=new Option("Skechers","Skechers");
        document.getElementById("thirdcategory").options[5]=new Option("Nike","Nike");
        break;
    
    case "Watches" :
        if($('#clothingcategory').length != 0){
            document.getElementById('clothingcategory').remove()
        }
        document.getElementById("thirdcategory").options[0]=new Option("No Watches Category","");
        document.getElementById("thirdcategory").options[5]=new Option("Casio","Casio");
        document.getElementById("thirdcategory").options[2]=new Option("Fossil","Fossil");
        document.getElementById("thirdcategory").options[1]=new Option("Samsung","Samsung");
        document.getElementById("thirdcategory").options[4]=new Option("Seiko","Seiko");
        document.getElementById("thirdcategory").options[3]=new Option("SUUNTO","SUUNTO");
        break;

    default:
        if($('#clothingcategory').length != 0){
            document.getElementById('clothingcategory').remove()
        }
        document.getElementById("thirdcategory").options[0]=new Option("No Category","");
        break;  
    }
    return true;
}

function dynamicdropdownclothing(listindex)
{
    document.getElementById("clothingcategory").length = 0;
    switch (listindex)
    {
    case "Shirt" :
        document.getElementById("clothingcategory").options[0]=new Option("No Shirt Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Carhartt","Carhartt");
        document.getElementById("clothingcategory").options[2]=new Option("Gildan","Gildan");
        document.getElementById("clothingcategory").options[3]=new Option("Under Armour","Sweaters");
        document.getElementById("clothingcategory").options[4]=new Option("Amazon Essentials","Amazon Essentials");
        break;

    case "Hoodies & Sweatshirts" :
        document.getElementById("clothingcategory").options[0]=new Option("No Hoodies & Sweatshirts Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Carhartt","Carhartt");
        document.getElementById("clothingcategory").options[2]=new Option("Gildan","Gildan");
        document.getElementById("clothingcategory").options[3]=new Option("Campus Colors","Campus Colors");
        document.getElementById("clothingcategory").options[4]=new Option("OHOO","OHOO");
        break;

    case "Sweaters" :
        document.getElementById("clothingcategory").options[0]=new Option("No Sweaters Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Amazon Essentials","Amazon Essentials");
        document.getElementById("clothingcategory").options[2]=new Option("poriff","poriff");
        document.getElementById("clothingcategory").options[3]=new Option("GIVON","GIVON");
        document.getElementById("clothingcategory").options[4]=new Option("Jerzees","Jerzees");
        break;

    case "Jacket & Coats" :
        document.getElementById("clothingcategory").options[0]=new Option("No Jacket & Coats Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Columbia","Columbia");
        document.getElementById("clothingcategory").options[2]=new Option("Champion","Champion");
        document.getElementById("clothingcategory").options[3]=new Option("Frogg","Frogg");
        document.getElementById("clothingcategory").options[4]=new Option("Anyoo","Anyoo");
        break;
    
    case "Jeans" :
        document.getElementById("clothingcategory").options[0]=new Option("No Jeans Category","");
        document.getElementById("clothingcategory").options[1]=new Option("UNIONBAY","UNIONBAY");
        document.getElementById("clothingcategory").options[2]=new Option("Fruit of the Loom","Fruit of the Loom");
        document.getElementById("clothingcategory").options[3]=new Option("Dickies","Dickies");
        document.getElementById("clothingcategory").options[4]=new Option("Carhart","Carhart");
        break;

    case "Pants" :
        document.getElementById("clothingcategory").options[0]=new Option("No Pants Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Haggar","Haggar");
        document.getElementById("clothingcategory").options[2]=new Option("Amazon Essentials","Amazon Essentials");
        document.getElementById("clothingcategory").options[3]=new Option("Dickies","Dickies");
        document.getElementById("clothingcategory").options[4]=new Option("UNIONBAY","UNIONBAY");
        break;

    case "Shorts" :
        document.getElementById("clothingcategory").options[0]=new Option("No Shorts Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Docker","Docker");
        document.getElementById("clothingcategory").options[2]=new Option("Amazon Essentials","Amazon Essentials");
        document.getElementById("clothingcategory").options[3]=new Option("Wrangler Authentics","Wrangler Authentics");
        document.getElementById("clothingcategory").options[4]=new Option("UNIONBAY","UNIONBAY");
        break;

    case "Active" :
        document.getElementById("clothingcategory").options[0]=new Option("No Active Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Dickies","Dickies");
        document.getElementById("clothingcategory").options[2]=new Option("Amazon Essentials","Amazon Essentials");
        document.getElementById("clothingcategory").options[3]=new Option("Hanes","Hanes");
        document.getElementById("clothingcategory").options[4]=new Option("Adidas","Adidas");
        break;

    case "Swim" :
        document.getElementById("clothingcategory").options[0]=new Option("No Swim Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Kanu Surf","Kanu Surf");
        document.getElementById("clothingcategory").options[2]=new Option("Amazon Essentials","Amazon Essentials");
        document.getElementById("clothingcategory").options[3]=new Option("Speedo","Speedo");
        document.getElementById("clothingcategory").options[4]=new Option("MaaMgic","MaaMgic");
        break;

    case "Suits & Sport Coats" :
        document.getElementById("clothingcategory").options[0]=new Option("No Suits & Sport Coats Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Kenneth Cole","Kenneth Cole");
        document.getElementById("clothingcategory").options[2]=new Option("Gioberti","Gioberti");
        document.getElementById("clothingcategory").options[3]=new Option("COOFANDY","COOFANDY");
        document.getElementById("clothingcategory").options[4]=new Option("Calvin Klein","Calvin Klein");
        break;

    case "Underwear" :
        document.getElementById("clothingcategory").options[0]=new Option("No Underwear Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Gildan","Gildan");
        document.getElementById("clothingcategory").options[2]=new Option("Calvin Klein","Calvin Klein");
        document.getElementById("clothingcategory").options[3]=new Option("Hanes","Hanes");
        document.getElementById("clothingcategory").options[4]=new Option("Adidas","Adidas");
        break;

    case "Socks" :
        document.getElementById("clothingcategory").options[0]=new Option("No Shirt Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Dickies","Dickies");
        document.getElementById("clothingcategory").options[2]=new Option("Balega","Balega");
        document.getElementById("clothingcategory").options[3]=new Option("Nike","Nike");
        document.getElementById("clothingcategory").options[4]=new Option("Adidas","Adidas");
        break;

    case "Sleep & Lounge" :
        document.getElementById("clothingcategory").options[0]=new Option("No Shirt Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Amazon Essentials","Amazon Essentials");
        document.getElementById("clothingcategory").options[2]=new Option("U2SKIIN","U2SKIIN");
        document.getElementById("clothingcategory").options[3]=new Option("NY Threads","NY Threads");
        document.getElementById("clothingcategory").options[4]=new Option("Burt's Bees","Burt's Bees");
        break;
        
    case "T-Shirts & Tanks" :
        document.getElementById("clothingcategory").options[0]=new Option("No Shirt Category","");
        document.getElementById("clothingcategory").options[1]=new Option("Carhartt","Carhartt");
        document.getElementById("clothingcategory").options[2]=new Option("Gildan","Gildan");
        document.getElementById("clothingcategory").options[3]=new Option("Fruit of the Loom","Fruit of the Loom");
        document.getElementById("clothingcategory").options[4]=new Option("Hanes","Hanes");
        break;

    default:
        document.getElementById("clothingcategory").options[0]=new Option("No Category","");
        break;  
    }
    return true;
}