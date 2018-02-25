!function(){
var calc = function(){
	var docEle = document.documentElement;
	var clientWidth = docEle.clientWidth > 750 ? 750 : docEle.clientWidth;
	docEle.style.fontSize = 20*(clientWidth/375) + 'px';
}
calc();
window.addEventListener('resize', calc)
}()