odoo.define('web.WebClient', function (require) {
    "use strict";
    
    var AbstractWebClient = require('web.AbstractWebClient');
    var data = require('web.data');
    var data_manager = require('web.data_manager');
    var Menu = require('web.Menu');
    var Model = require('web.DataModel');
    var session = require('web.session');
    var SystrayMenu = require('web.SystrayMenu');
    var UserMenu = require('web.UserMenu');
    
    return AbstractWebClient.extend({
        events: {
            'click #oe_main_menu_navbar .toggle-menu-icon': 'toggle_menu',
            'click #fabric_app_menu > .hitbox': 'toggle_menu',
            'click #fabric_app_menu ul.menus > li > a': 'toggle_menu',
            'click #toggle_sub_menu': 'toggle_sub_menu',
            'click .o_main.rs-open .o_sub_menu .oe_secondary_menu a:not(".oe_menu_toggler")': 'toggle_sub_menu',
        },
        show_application: function() {
            var self = this;
    
            // Allow to call `on_attach_callback` and `on_detach_callback` when needed
            this.action_manager.is_in_DOM = true;
    
            this.toggle_bars(true);
            this.set_title();
    
            // Menu is rendered server-side thus we don't want the widget to create any dom
            this.menu = new Menu(this);
            this.menu.setElement(this.$el.find('#fabric_app_menu'));
            this.menu.on('menu_click', this, this.on_menu_action);
    
            // Create the user menu (rendered client-side)
            this.user_menu = new UserMenu(this);
            var $user_menu_placeholder = $('body').find('.oe_user_menu_placeholder').show();
            var user_menu_loaded = this.user_menu.appendTo($user_menu_placeholder);
    
            // Create the systray menu (rendered server-side)
            this.systray_menu = new SystrayMenu(this);
            this.systray_menu.setElement(this.$el.parents().find('.oe_systray'));
            var systray_menu_loaded = this.systray_menu.start();
    
            // Start the menu once both systray and user menus are rendered
            // to prevent overflows while loading
            return $.when(systray_menu_loaded, user_menu_loaded).then(function() {
                self.menu.start();
                self.bind_hashchange();
            });
    
        },
        toggle_bars: function(value) {
            this.$('tr:has(td.navbar),.oe_leftbar').toggle(value);
        },
        toggle_menu: function(ev) {
            ev.preventDefault();
            this.$('#fabric_app_menu').toggle()
            this.$el.find('#oe_main_menu_navbar > .toggle-menu-icon').toggleClass('open')
        },
        toggle_sub_menu: function(ev) {
            var self = this;
            if (ev) {
                ev.preventDefault();
            }
            var $main = this.$el.parents().find('.o_web_client > .o_main')
            if ($main.hasClass('rs-open')) {
                $main.removeClass('rs-open')
            } else {
                $main.addClass('rs-open');
                if ($main.find('> .backdrop').length === 0) {
                    $main.append(function() {
                        return $('<div class="backdrop" />').on('click', function() {
                            self.toggle_sub_menu()
                        })
                    })
                }
            }
        },
        bind_hashchange: function() {
            var self = this;
            $(window).bind('hashchange', this.on_hashchange);
    
            var state = $.bbq.getState(true);
            if (_.isEmpty(state) || state.action === "login") {
                self.menu.is_bound.done(function() {
                    new Model("res.users").call("read", [[session.uid], ["action_id"]]).done(function(result) {
                        var data = result[0];
                        if(data.action_id) {
                            self.action_manager.do_action(data.action_id[0]);
                            self.menu.open_action(data.action_id[0]);
                        } else {
                            var first_menu_id = self.menu.$el.find("a:first").data("menu");
                            if(first_menu_id) {
                                self.menu.menu_click(first_menu_id);
                            }
                        }
                    });
                });
            } else {
                $(window).trigger('hashchange');
            }
        },
        on_hashchange: function(event) {
            if (this._ignore_hashchange) {
                this._ignore_hashchange = false;
                return;
            }
    
            var self = this;
            this.clear_uncommitted_changes().then(function () {
                var stringstate = event.getState(false);
                if (!_.isEqual(self._current_state, stringstate)) {
                    var state = event.getState(true);
                    if(!state.action && state.menu_id) {
                        self.menu.is_bound.done(function() {
                            self.menu.menu_click(state.menu_id);
                        });
                    } else {
                        state._push_me = false;  // no need to push state back...
                        self.action_manager.do_load_state(state, !!self._current_state).then(function () {
                            var action = self.action_manager.get_inner_action();
                            if (action) {
                                self.menu.open_action(action.action_descr.id);
                            }
                        });
                    }
                }
                self._current_state = stringstate;
            }, function () {
                if (event) {
                    self._ignore_hashchange = true;
                    window.location = event.originalEvent.oldURL;
                }
            });
        },
        on_menu_action: function(options) {
            var self = this;
            return this.menu_dm.add(data_manager.load_action(options.action_id))
                .then(function (result) {
                    return self.action_mutex.exec(function() {
                        if (options.needaction) {
                            result.context = new data.CompoundContext(result.context, {
                                search_default_message_needaction: true,
                                search_disable_custom_filters: true,
                            });
                        }
                        var completed = $.Deferred();
                        $.when(self.action_manager.do_action(result, {
                            clear_breadcrumbs: true,
                            action_menu_id: self.menu.current_menu,
                        })).fail(function() {
                            self.menu.open_menu(options.previous_menu_id);
                        }).always(function() {
                            completed.resolve();
                        });
                        setTimeout(function() {
                            completed.resolve();
                        }, 2000);
                        // We block the menu when clicking on an element until the action has correctly finished
                        // loading. If something crash, there is a 2 seconds timeout before it's unblocked.
                        return completed;
                    });
                });
        },
    });
    
    });
    