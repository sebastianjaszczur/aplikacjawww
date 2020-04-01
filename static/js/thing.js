$(function() {
    function colorChange()
    {
        $(".navbar").css("background", '#'+((1<<24)*(Math.random()+1)|0).toString(16).substr(1));
    }

    var active = false;
    function activateEgg()
    {
        if (active)
            return;
        active = true;
        colorChange();
        setInterval(colorChange, 3000);
        $("body").mousedown(colorChange);
        $("body").keydown(colorChange);
    }

    new Konami(activateEgg);

    var today = new Date();
    if(today.getDate() == 1 && today.getMonth()+1 == 4)
        activateEgg();
});