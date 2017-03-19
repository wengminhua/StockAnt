$.easing.doubleSqrt = function(t, millisecondsSince, startValue, endValue, totalDuration) {
    var res = Math.sqrt(Math.sqrt(t));
    return res;
};

(function($) {

    $.tileBlockSlider = function(element, options) {

        // §ß§Ñ§ã§ä§â§à§Û§Ü§Ú §á§à §å§Þ§à§Ý§é§Ñ§ß§Ú§ð
        var defaults = {
            // §á§Ö§â§Ú§à§Õ §ã§Þ§Ö§ß§í §Ü§Ñ§â§ä§Ú§ß§à§Ü
            period: 2000,
            // §á§â§à§Õ§à§Ý§Ø§Ú§ä§Ö§Ý§î§ß§à§ã§ä§î §Ñ§ß§Ú§Þ§Ñ§è§Ú§Ú
            duration: 1000,
            // §ß§Ñ§á§â§Ñ§Ó§Ý§Ö§ß§Ú§Ö §Ñ§ß§Ú§Þ§Ñ§è§Ú§Ú (up, down, left, right)
            direction: 'up'
        };
        // §à§Ò§ì§Ö§Ü§ä §á§Ý§Ñ§Ô§Ú§ß§Ñ
        var plugin = this;
        // §ß§Ñ§ã§ä§â§à§Û§Ü§Ú §Ü§à§ß§Ü§â§Ö§ä§ß§à§Ô§à §à§Ò§ì§Ö§Ü§ä§Ñ
        plugin.settings = {};

        var $element = $(element), // reference to the jQuery version of DOM element
            element = element;    // reference to the actual DOM element

        var blocks, // §Ó§ã§Ö §Ü§Ñ§â§ä§Ú§ß§Ü§Ú
            currentBlockIndex, // §Ú§ß§Õ§Ö§Ü§ã §ä§Ö§Ü§å§ë§Ö§Ô§à §Ò§Ý§à§Ü§Ñ
            slideInPosition, // §ã§ä§Ñ§â§ä§à§Ó§à§Ö §á§à§Ý§à§Ø§Ö§ß§Ú§Ö §Ò§Ý§à§Ü§Ñ §á§Ö§â§Ö§Õ §ß§Ñ§é§Ñ§Ý§à§Þ §á§à§ñ§Ó§Ý§Ö§ß§Ú§ñ
            slideOutPosition, // §æ§Ú§ß§Ñ§Ý§î§ß§à§Ö §á§à§Ý§à§Ø§Ö§ß§Ú§Ö §Ò§Ý§à§Ü§Ñ §á§â§Ú §ã§Ü§â§í§ä§Ú§Ú
            tileWidth, // §â§Ñ§Ù§Þ§Ö§â§í §á§Ý§Ú§ä§Ü§Ú
            tileHeight;

        // §Ú§ß§Ú§è§Ú§Ñ§Ý§Ú§Ù§Ú§â§å§Ö§Þ
        plugin.init = function () {

            plugin.settings = $.extend({}, defaults, options);

            // §Ó§ã§Ö §Ò§Ý§à§Ü§Ú
            blocks = $element.children(".tile-content");

            // §Ö§ã§Ý§Ú §Ò§Ý§à§Ü §Ó§ã§Ö§Ô§à 1, §ä§à §ã§Ý§Ñ§Û§Õ§Ú§ß§Ô §ß§Ö §ß§å§Ø§Ö§ß
            if (blocks.length <= 1) {
                return;
            }

            // §Ú§ß§Õ§Ö§Ü§ã §Ñ§Ü§ä§Ú§Ó§ß§à§Ô§à §Ó §Õ§Ñ§ß§ß§í§Û §Þ§à§Þ§Ö§ß§ä §Ò§Ý§à§Ü§Ñ
            currentBlockIndex = 0;

            // §â§Ñ§Ù§Þ§Ö§â§í §ä§Ö§Ü§å§ë§Ö§Û §á§Ý§Ú§ä§Ü§Ú
            tileWidth = $element.innerWidth();
            tileHeight = $element.innerHeight();
            // §á§à§Ý§à§Ø§Ö§ß§Ú§Ö §Ò§Ý§à§Ü§à§Ó
            slideInPosition = getSlideInPosition();
            slideOutPosition = getSlideOutPosition();

            // §á§à§Õ§Ô§à§ä§Ñ§Ó§Ý§Ú§Ó§Ñ§Ö§Þ §Ò§Ý§à§Ü§Ú §Ü §Ñ§ß§Ú§Þ§Ñ§è§Ú§Ú
            blocks.each(function (index, block) {
                block = $(block);
                // §Ò§Ý§à§Ü§Ú §Õ§à§Ý§Ø§ß§í §Ò§í§ä§î position:absolute
                // §Ó§à§Ù§Þ§à§Ø§ß§à §ï§ä§à§ä §á§Ñ§â§Ñ§Þ§Ö§ä§â §Ù§Ñ§Õ§Ñ§ß §é§Ö§â§Ö§Ù §Ü§Ý§Ñ§ã§ã §ã§ä§Ú§Ý§Ö§Û
                // §á§â§à§Ó§Ö§â§ñ§Ö§Þ, §Ú §Õ§à§Ò§Ñ§Ó§Ý§ñ§Ö§Þ §Ö§ã§Ý§Ú §ï§ä§à §ß§Ö §ä§Ñ§Ü
                if (block.css('position') !== 'absolute') {
                    block.css('position', 'absolute');
                }
                // §ã§Ü§â§í§Ó§Ñ§Ö§Þ §Ó§ã§Ö §Ò§Ý§à§Ü§Ú §Ü§â§à§Þ§Ö §á§Ö§â§Ó§à§Ô§à
                if (index !== 0) {
                    block.css('left', tileWidth);
                }
            });

            // §Ù§Ñ§á§å§ã§Ü§Ñ§Ö§Þ §Ú§ß§ä§Ö§â§Ó§Ñ§Ý §Õ§Ý§ñ §ã§Þ§Ö§ß§í §Ò§Ý§à§Ü§à§Ó
            setInterval(function () {
                slideBlock();
            }, plugin.settings.period);
        };

        // §ã§Þ§Ö§ß§Ñ §Ò§Ý§à§Ü§à§Ó
        var slideBlock = function() {

            var slideOutBlock, // §Ò§Ý§à§Ü §Ü§à§ä§à§â§í§Û §ß§Ñ§Õ§à §ã§Ü§â§í§ä§î
                slideInBlock, // §Ò§Ý§à§Ü §Ü§à§ä§à§â§í§Û §ß§Ñ§Õ§à §á§à§Ü§Ñ§Ù§Ñ§ä§î
                mainPosition = {'left': 0, 'top': 0},
                options;

            slideOutBlock = $(blocks[currentBlockIndex]);

            currentBlockIndex++;
            if (currentBlockIndex >= blocks.length) {
                currentBlockIndex = 0;
            }
            slideInBlock = $(blocks[currentBlockIndex]);

            slideInBlock.css(slideInPosition);

            options = {
                duration: plugin.settings.duration,
                easing: 'doubleSqrt'
            };

            slideOutBlock.animate(slideOutPosition, options);
            slideInBlock.animate(mainPosition, options);
        };

        /**
         * §Ó§à§Ù§Ó§â§Ñ§ë§Ñ§Ö§ä §ã§ä§Ñ§â§ä§à§Ó§å§ð §á§à§Ù§Ú§è§Ú§ð §Õ§Ý§ñ §Ò§Ý§à§Ü§Ñ §Ü§à§ä§à§â§í§Û §Õ§à§Ý§Ø§Ö§ß §á§à§ñ§Ó§Ú§ä§î§ã§ñ {left: xxx, top: yyy}
         */
        var getSlideInPosition = function () {
            var pos;
            if (plugin.settings.direction === 'left') {
                pos = {
                    'left': tileWidth,
                    'top': 0
                }
            } else if (plugin.settings.direction === 'right') {
                pos = {
                    'left': -tileWidth,
                    'top': 0
                }
            } else if (plugin.settings.direction === 'up') {
                pos = {
                    'left': 0,
                    'top': tileHeight
                }
            } else if (plugin.settings.direction === 'down') {
                pos = {
                    'left': 0,
                    'top': -tileHeight
                }
            }
            return pos;
        };

        /**
         * §Ó§à§Ù§Ó§â§Ñ§ë§Ñ§Ö§ä §æ§Ú§ß§Ñ§Ý§î§ß§å§ð §á§à§Ù§Ú§è§Ú§ð §Õ§Ý§ñ §Ò§Ý§à§Ü§Ñ §Ü§à§ä§à§â§í§Û §Õ§à§Ý§Ø§Ö§ß §ã§Ü§â§í§ä§î§ã§ñ {left: xxx, top: yyy}
         */
        var getSlideOutPosition = function () {
            var pos;
            if (plugin.settings.direction === 'left') {
                pos = {
                    'left': -tileWidth,
                    'top': 0
                }
            } else if (plugin.settings.direction === 'right') {
                pos = {
                    'left': tileWidth,
                    'top': 0
                }
            } else if (plugin.settings.direction === 'up') {
                pos = {
                    'left': 0,
                    'top': -tileHeight
                }
            } else if (plugin.settings.direction === 'down') {
                pos = {
                    'left': 0,
                    'top': tileHeight
                }
            }
            return pos;
        };

        plugin.getParams = function() {

            // code goes here

        }

        plugin.init();

    }

    $.fn.tileBlockSlider = function(options) {
        return this.each(function() {
            if (undefined == $(this).data('tileBlockSlider')) {
                var plugin = new $.tileBlockSlider(this, options);
                $(this).data('tileBlockSlider', plugin);
            }
        });
    }

})(jQuery);


$(window).ready(function(){
    var slidedTiles = $('[data-role=tile-slider], .block-slider, .tile-slider');
    slidedTiles.each(function (index, tile) {
        var params = {};
        tile = $(tile);
        params.direction = tile.data('paramDirection');
        params.duration = tile.data('paramDuration');
        params.period = tile.data('paramPeriod');
        tile.tileBlockSlider(params);
    })

});