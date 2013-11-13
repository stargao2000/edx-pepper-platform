// Generated by CoffeeScript 1.6.3
(function() {
  describe('Logger', function() {
    it('expose window.log_event', function() {
      return expect(window.log_event).toBe(Logger.log);
    });
    describe('log', function() {
      return it('send a request to log event', function() {
        spyOn($, 'postWithPrefix');
        Logger.log('example', 'data');
        return expect($.postWithPrefix).toHaveBeenCalledWith('/event', {
          event_type: 'example',
          event: '"data"',
          page: window.location.href
        });
      });
    });
    return xdescribe('bind', function() {
      beforeEach(function() {
        Logger.bind();
        return Courseware.prefix = '/6002x';
      });
      afterEach(function() {
        return window.onunload = null;
      });
      it('bind the onunload event', function() {
        return expect(window.onunload).toEqual(jasmine.any(Function));
      });
      return it('send a request to log event', function() {
        spyOn($, 'ajax');
        window.onunload();
        return expect($.ajax).toHaveBeenCalledWith({
          url: "" + Courseware.prefix + "/event",
          data: {
            event_type: 'page_close',
            event: '',
            page: window.location.href
          },
          async: false
        });
      });
    });
  });

}).call(this);