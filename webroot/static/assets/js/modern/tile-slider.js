$.easing.doubleSqrt = function(t, millisecondsSince, startValue, endValue, totalDuration) {
    var res = Math.sqrt(Math.sqrt(t));
    return res;
};

(function($) {

    $.tileBlockSlider = function(element, options) {

        // �ߧѧ����ۧܧ� ��� ��ާ�ݧ�ѧߧڧ�
        var defaults = {
            // ��֧�ڧ�� ��ާ֧ߧ� �ܧѧ��ڧߧ��
            period: 2000,
            // ����է�ݧاڧ�֧ݧ�ߧ���� �ѧߧڧާѧ�ڧ�
            duration: 1000,
            // �ߧѧ��ѧӧݧ֧ߧڧ� �ѧߧڧާѧ�ڧ� (up, down, left, right)
            direction: 'up'
        };
        // ��ҧ�֧ܧ� ��ݧѧԧڧߧ�
        var plugin = this;
        // �ߧѧ����ۧܧ� �ܧ�ߧܧ�֧�ߧ�ԧ� ��ҧ�֧ܧ��
        plugin.settings = {};

        var $element = $(element), // reference to the jQuery version of DOM element
            element = element;    // reference to the actual DOM element

        var blocks, // �ӧ�� �ܧѧ��ڧߧܧ�
            currentBlockIndex, // �ڧߧէ֧ܧ� ��֧ܧ��֧ԧ� �ҧݧ�ܧ�
            slideInPosition, // ���ѧ���ӧ�� ���ݧ�ا֧ߧڧ� �ҧݧ�ܧ� ��֧�֧� �ߧѧ�ѧݧ�� ����ӧݧ֧ߧڧ�
            slideOutPosition, // ��ڧߧѧݧ�ߧ�� ���ݧ�ا֧ߧڧ� �ҧݧ�ܧ� ���� ��ܧ���ڧ�
            tileWidth, // ��ѧ٧ާ֧�� ��ݧڧ�ܧ�
            tileHeight;

        // �ڧߧڧ�ڧѧݧڧ٧ڧ��֧�
        plugin.init = function () {

            plugin.settings = $.extend({}, defaults, options);

            // �ӧ�� �ҧݧ�ܧ�
            blocks = $element.children(".tile-content");

            // �֧�ݧ� �ҧݧ�� �ӧ�֧ԧ� 1, ��� ��ݧѧۧէڧߧ� �ߧ� �ߧ�ا֧�
            if (blocks.length <= 1) {
                return;
            }

            // �ڧߧէ֧ܧ� �ѧܧ�ڧӧߧ�ԧ� �� �էѧߧߧ�� �ާ�ާ֧ߧ� �ҧݧ�ܧ�
            currentBlockIndex = 0;

            // ��ѧ٧ާ֧�� ��֧ܧ��֧� ��ݧڧ�ܧ�
            tileWidth = $element.innerWidth();
            tileHeight = $element.innerHeight();
            // ���ݧ�ا֧ߧڧ� �ҧݧ�ܧ��
            slideInPosition = getSlideInPosition();
            slideOutPosition = getSlideOutPosition();

            // ���էԧ��ѧӧݧڧӧѧ֧� �ҧݧ�ܧ� �� �ѧߧڧާѧ�ڧ�
            blocks.each(function (index, block) {
                block = $(block);
                // �ҧݧ�ܧ� �է�ݧاߧ� �ҧ��� position:absolute
                // �ӧ�٧ާ�اߧ� ����� ��ѧ�ѧާ֧�� �٧ѧէѧ� ��֧�֧� �ܧݧѧ�� ���ڧݧ֧�
                // ����ӧ֧��֧�, �� �է�ҧѧӧݧ�֧� �֧�ݧ� ���� �ߧ� ��ѧ�
                if (block.css('position') !== 'absolute') {
                    block.css('position', 'absolute');
                }
                // ��ܧ��ӧѧ֧� �ӧ�� �ҧݧ�ܧ� �ܧ��ާ� ��֧�ӧ�ԧ�
                if (index !== 0) {
                    block.css('left', tileWidth);
                }
            });

            // �٧ѧ���ܧѧ֧� �ڧߧ�֧�ӧѧ� �էݧ� ��ާ֧ߧ� �ҧݧ�ܧ��
            setInterval(function () {
                slideBlock();
            }, plugin.settings.period);
        };

        // ��ާ֧ߧ� �ҧݧ�ܧ��
        var slideBlock = function() {

            var slideOutBlock, // �ҧݧ�� �ܧ������ �ߧѧէ� ��ܧ����
                slideInBlock, // �ҧݧ�� �ܧ������ �ߧѧէ� ���ܧѧ٧ѧ��
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
         * �ӧ�٧ӧ�ѧ�ѧ֧� ���ѧ���ӧ�� ���٧ڧ�ڧ� �էݧ� �ҧݧ�ܧ� �ܧ������ �է�ݧا֧� ����ӧڧ���� {left: xxx, top: yyy}
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
         * �ӧ�٧ӧ�ѧ�ѧ֧� ��ڧߧѧݧ�ߧ�� ���٧ڧ�ڧ� �էݧ� �ҧݧ�ܧ� �ܧ������ �է�ݧا֧� ��ܧ������ {left: xxx, top: yyy}
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