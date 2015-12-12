define(["./core","./selector","./traversing","./callbacks","./deferred","./core/ready","./support","./data","./queue","./queue/delay","./attributes","./event","./event/alias","./manipulation","./manipulation/_evalUrl","./wrap","./css","./css/hiddenVisibleSelectors","./serialize","./ajax","./ajax/xhr","./ajax/script","./ajax/jsonp","./ajax/load","./event/ajax","./effects","./effects/animatedSelector","./offset","./dimensions","./deprecated","./exports/amd","./exports/global"],function(e){return e}),function(e){"function"==typeof define&&define.amd?define(["jquery"],e):"undefined"!=typeof module&&null!==module&&module.exports?module.exports=e:e(jQuery)}(function(e,t){function i(e){var t,i,s;t=e.currentTarget.offsetWidth,i=e.currentTarget.offsetHeight,s={distX:e.distX,distY:e.distY,velocityX:e.velocityX,velocityY:e.velocityY,finger:e.finger},e.distX>e.distY?e.distX>-e.distY?(e.distX/t>d.threshold||e.velocityX*e.distX/t*d.sensitivity>1)&&(s.type="swiperight",a(e.currentTarget,s)):(-e.distY/i>d.threshold||e.velocityY*e.distY/t*d.sensitivity>1)&&(s.type="swipeup",a(e.currentTarget,s)):e.distX>-e.distY?(e.distY/i>d.threshold||e.velocityY*e.distY/t*d.sensitivity>1)&&(s.type="swipedown",a(e.currentTarget,s)):(-e.distX/t>d.threshold||e.velocityX*e.distX/t*d.sensitivity>1)&&(s.type="swipeleft",a(e.currentTarget,s))}function s(t){var i=e.data(t,"event_swipe");return i||(i={count:0},e.data(t,"event_swipe",i)),i}var n=e.event.add,r=e.event.remove,a=function(t,i,s){e.event.trigger(i,s,t)},d={threshold:.4,sensitivity:6};e.event.special.swipe=e.event.special.swipeleft=e.event.special.swiperight=e.event.special.swipeup=e.event.special.swipedown={setup:function(e,t,r){var e=s(this);if(!(e.count++>0))return n(this,"moveend",i),!0},teardown:function(){var e=s(this);if(!(--e.count>0))return r(this,"moveend",i),!0},settings:d}});