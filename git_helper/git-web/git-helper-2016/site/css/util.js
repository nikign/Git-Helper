//use for show more paragraph
function showmore(){
  console.log("test show more");
  var $this = $(this);
  var $content = $this.parent().prev("div.content");
  var linkText = $this.text().toUpperCase();

  console.log("content:"+$content);
  console.log(linkText);
  if(linkText === "...MORE"){
      linkText = "...less";
      $content.switchClass("hideContent", "showContent", 400);
  } else {
      linkText = "...more";
      $content.switchClass("showContent", "hideContent", 400);
  };
  $this.text(linkText);
  console.log("test show more");
};
//=========================================
function isHelpful(link,key) {
    $.ajax({
      type:"POST",
      url:"/storeClickLog",
      data:{
        "errorMessage":key,
        "link": link
      }
    }).done(function(){
//      var x;
//      if (confirm("Does this link helpful?") == true) {
//          x = "Yes";
//      } else {
//          x = "No";
//      }
    });
};

function rateLink(link,key,isHelpful,id) {
    if(isHelpful == "yes")
    {
      document.getElementById("yes"+id).style.backgroundColor = "#009A00";
      document.getElementById("no"+id).style.backgroundColor = "#FFFFFF";
    }
    else
    {
      document.getElementById("no"+id).style.backgroundColor = "#9A9A9A";
      document.getElementById("yes"+id).style.backgroundColor = "#FFFFFF";
    }
    $.ajax({
      type:"POST",
      url:"/rateLink",
      data:{
        "errorMessage":key,
        "link": link,
        "helpful": isHelpful
      }
    });
};
