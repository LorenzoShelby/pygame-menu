# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST MENU
Menu object tests.

NOTE: pygame-menu v3 will not provide new widgets or functionalities, consider
upgrading to the latest version.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

from test._utils import *

from pygame_menu import events
from pygame_menu.widgets import Label, Button
import pygame
import timeit

# Configure the tests
_TEST_TIME_DRAW = False


class MenuTest(unittest.TestCase):

    def setUp(self):
        """
        Test setup.
        """
        test_reset_surface()
        self.menu = MenuUtils.generic_menu(title='mainmenu')
        self.menu.mainloop(surface, bgfun=dummy_function)

    @staticmethod
    def test_time_draw():
        """
        This test the time that takes to pygame_menu to draw several times.
        """
        if not _TEST_TIME_DRAW:
            return
        menu = MenuUtils.generic_menu(title='EPIC')
        menu.enable()

        # Add several widgets
        for i in range(30):
            menu.add_button(title='epic', action=events.BACK)
            menu.add_vertical_margin(margin=10)
            menu.add_label(title='epic test')
            menu.add_color_input(title='color', color_type='rgb', default=(234, 33, 2))
            menu.add_selector(title='epic selector', items=[('1', '3'), ('2', '4')])
            menu.add_text_input(title='text', default='the default text')

        print(timeit.timeit(lambda: menu.draw(surface), number=100))

    def test_size(self):
        """
        Test menu sizes.
        """
        inf_size = 1000000000
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=0, height=300))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=300, height=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=-200, height=300))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=inf_size, height=300))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=300, height=inf_size))

    def test_position(self):
        """
        Test position.
        """
        # Test centering
        menu = MenuUtils.generic_menu()
        btn = menu.add_button('button', None)
        menu.center_content()
        self.assertEqual(menu.get_height(), 400)
        self.assertEqual(menu.get_height(inner=True), 345)
        self.assertEqual(menu.get_menubar_widget().get_height(), 55)

        h = 41
        if pygame.version.vernum[0] < 2:
            h = 42

        self.assertEqual(btn.get_height(), h)
        self.assertEqual(btn.get_size()[1], h)
        self.assertEqual(menu.get_height(widget=True), h)

        v_pos = int((345 - h) / 2)  # available_height - widget_height
        self.assertEqual(menu._widget_offset[1], v_pos)
        self.assertEqual(btn.get_position()[1], v_pos + 1)

        # If there's too many widgets, the centering should be disabled
        for i in range(20):
            menu.add_button('button', None)
        self.assertEqual(menu._widget_offset[1], 0)

        theme = menu.get_theme()

        # Anyway, as the widget is 0, the first button position should be the height of its selection effect
        btneff = btn.get_selection_effect().get_margin()[0]
        self.assertEqual(btn.get_position()[1], btneff + 1)

        self.assertEqual(h * 21 + theme.widget_margin[1] * 20, menu.get_height(widget=True))

        # Test menu not centered
        menu = MenuUtils.generic_menu(center_content=False)
        btn = menu.add_button('button', None)
        btneff = btn.get_selection_effect().get_margin()[0]
        self.assertEqual(btn.get_position()[1], btneff + 1)

        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=-1, position_y=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=0, position_y=-1))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=-1, position_y=-1))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=101, position_y=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=99, position_y=101))
        menu = MenuUtils.generic_menu(position_x=0, position_y=0)
        menu.set_relative_position(20, 40)

        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.widget_font_size = 20

        menu = pygame_menu.Menu(
            column_max_width=[380, 380],
            columns=2,
            height=300,
            rows=4,
            theme=theme,
            title='Welcome',
            width=400
        )

        quit1 = menu.add_button('Quit', pygame_menu.events.EXIT)
        name1 = menu.add_text_input('Name: ', default='John Doe', maxchar=10, padding=30)
        sel1 = menu.add_selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
        sel2 = menu.add_selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
        play1 = menu.add_button('Play', pygame_menu.events.NONE, align=pygame_menu.locals.ALIGN_LEFT)
        hidden = menu.add_button('Hidden', None, font_size=100)
        hidden.hide()
        quit2 = menu.add_button('Quit', pygame_menu.events.EXIT)
        label = menu.add_label('This label is really epic')
        label.rotate(90)

        menu.render()
        # menu.mainloop(surface)

        x, y = quit1.get_position()
        self.assertEqual(x, 170)
        self.assertEqual(y, 6)
        x, y = name1.get_position()
        self.assertEqual(x, 115)
        self.assertEqual(y, 74)
        x, y = sel1.get_position()
        self.assertEqual(x, 104)
        self.assertEqual(y, 142)
        x, y = sel2.get_position()
        self.assertEqual(x, 104)
        self.assertEqual(y, 180)
        x, y = play1.get_position()
        self.assertEqual(x, 389)
        self.assertEqual(y, 6)
        x, y = hidden.get_position()
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        x, y = quit2.get_position()
        self.assertEqual(x, 550)
        self.assertEqual(y, 44)
        x, y = label.get_position()
        self.assertEqual(x, 556)
        self.assertEqual(y, 82)

        # Test no selectable position
        menu = MenuUtils.generic_menu(center_content=False)
        btn = menu.add_button('button', None)
        btn.is_selectable = False
        menu.render()
        self.assertEqual(btn.get_position()[1], 1)

        # Test no selectable + widget
        menu = MenuUtils.generic_menu()
        img = menu.add_image(
            pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU,
            scale=(0.25, 0.25),
            align=pygame_menu.locals.ALIGN_CENTER
        )
        btn = menu.add_button('Nice', None)
        margin = menu.get_theme().widget_margin[1]
        menu.render()
        self.assertEqual(menu.get_height(widget=True), img.get_height() + btn.get_height() + margin)
        self.assertEqual(int((menu.get_height(inner=True) - menu.get_height(widget=True)) / 2), menu._widget_offset[1])

    def test_attributes(self):
        """
        Test menu attributes.
        """
        menu = MenuUtils.generic_menu()
        self.assertFalse(menu.has_attribute('epic'))
        self.assertRaises(IndexError, lambda: menu.remove_attribute('epic'))
        menu.set_attribute('epic', True)
        self.assertTrue(menu.has_attribute('epic'))
        self.assertTrue(menu.get_attribute('epic'))
        menu.set_attribute('epic', False)
        self.assertFalse(menu.get_attribute('epic'))
        menu.remove_attribute('epic')
        self.assertFalse(menu.has_attribute('epic'))
        self.assertEqual(menu.get_attribute('epic', 420), 420)

    def test_close(self):
        """
        Test menu close.
        """
        menu = MenuUtils.generic_menu()
        menu.set_attribute('epic', False)
        menu._back()

        def test_close():
            menu.set_attribute('epic', True)

        menu.set_onclose(test_close)
        self.assertTrue(not menu.is_enabled())
        menu.enable()
        self.assertFalse(menu.get_attribute('epic'))
        menu._close()
        self.assertTrue(menu.get_attribute('epic'))

    # noinspection PyArgumentEqualDefault
    def test_events(self):
        """
        Test events gather.
        """
        if pygame.vernum[0] < 2:
            return
        menu_top = MenuUtils.generic_menu()
        menu = MenuUtils.generic_menu(columns=4, rows=2, touchscreen_enabled=True,
                                      touchscreen_motion_selection=True,
                                      joystick_enabled=True)  # submenu
        menu_top.add_button('menu', menu).apply()
        widg = []
        for i in range(8):
            b = menu.add_button('test' + str(i), None)
            widg.append(b)
        # btn0 | btn2 | btn4 | btn6
        # btn1 | btn3 | btn5 | btn7
        self.assertEqual(menu_top.get_current(), menu)

        # Arrow keys
        menu_top.mainloop(surface)
        self.assertEqual(menu.get_selected_widget(), widg[0])
        menu_top.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), widg[0])
        menu_top.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu_top.update(PygameUtils.key(pygame_menu.controls.KEY_RIGHT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), widg[3])
        menu_top.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(menu.get_selected_widget(), widg[2])

        # Joy key
        menu_top.update(PygameUtils.joy_key(pygame_menu.controls.JOY_LEFT))
        self.assertEqual(menu.get_selected_widget(), widg[0])
        menu_top.update(PygameUtils.joy_key(pygame_menu.controls.JOY_DOWN))
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu_top.update(PygameUtils.joy_key(pygame_menu.controls.JOY_RIGHT))
        self.assertEqual(menu.get_selected_widget(), widg[3])
        menu_top.update(PygameUtils.joy_key(pygame_menu.controls.JOY_UP))
        self.assertEqual(menu.get_selected_widget(), widg[2])

        # Joy hat
        menu_top.update(PygameUtils.joy_motion(-10, 0))
        menu_top.enable()
        self.assertEqual(menu_top.get_current()._joy_event, menu._joy_event_left)
        self.assertEqual(menu.get_selected_widget(), widg[0])
        menu_top.update(PygameUtils.joy_motion(0, 10))
        self.assertEqual(menu_top.get_current()._joy_event, menu._joy_event_down)
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu_top.update(PygameUtils.joy_motion(10, 0))
        self.assertEqual(menu_top.get_current()._joy_event, menu._joy_event_right)
        self.assertEqual(menu.get_selected_widget(), widg[3])
        menu_top.update(PygameUtils.joy_motion(0, -10))
        self.assertEqual(menu_top.get_current()._joy_event, menu._joy_event_up)
        self.assertEqual(menu.get_selected_widget(), widg[2])

        # Menu should keep a recursive state of joy
        self.assertNotEqual(menu.get_current()._joy_event, 0)
        menu_top.update(PygameUtils.center_joy())  # center !!
        self.assertEqual(menu.get_current()._joy_event, 0)

        # Click widget
        menu_top.enable()
        menu_top.update(
            [PygameUtils.middle_rect_click(widg[1].get_rect(), menu_top, evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu_top.update(
            [PygameUtils.middle_rect_click(widg[0].get_rect(), menu_top, evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertEqual(menu.get_selected_widget(), widg[0])
        menu_top.update(
            [PygameUtils.middle_rect_click(widg[1].get_rect(), menu_top, evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertEqual(menu.get_selected_widget(), widg[1])

        # It should not change the menu selection (button up)
        self.assertTrue(
            menu_top.update([PygameUtils.middle_rect_click(widg[1].get_rect(), menu, evtype=pygame.MOUSEBUTTONUP)]))
        self.assertEqual(menu.get_selected_widget(), widg[1])

        # Applying button up in a non-selected widget must return false
        self.assertFalse(
            menu.update([PygameUtils.middle_rect_click(widg[0].get_rect(), menu, evtype=pygame.MOUSEBUTTONUP)]))

        # Fingerdown don't change selected widget if _touchscreen_motion_selection is enabled
        self.assertTrue(menu._touchscreen_motion_selection)
        menu.update([PygameUtils.middle_rect_click(widg[0].get_rect(), menu_top, evtype=pygame.FINGERDOWN)])
        # self.assertNotEqual(menu.get_selected_widget(), widg[0])

        # If touchscreen motion is disabled, then fingerdown should select the widget
        menu._touchscreen_motion_selection = False
        menu.update([PygameUtils.middle_rect_click(widg[1].get_rect(), menu_top, evtype=pygame.FINGERDOWN)])
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu._touchscreen_motion_selection = True

        # Fingermotion should select widgets as touchscreen is active
        menu.update([PygameUtils.middle_rect_click(widg[0].get_rect(), menu_top, evtype=pygame.FINGERMOTION)])
        self.assertEqual(menu.get_selected_widget(), widg[0])

        # Infinite joy
        menu_top.update(PygameUtils.joy_motion(0, 10))
        menu.update([pygame.event.Event(menu._joy_event_repeat)])
        self.assertNotEqual(menu._joy_event, 0)

        # Now disable joy event, then event repeat should not continue
        menu._joy_event = 0
        menu.update([pygame.event.Event(menu._joy_event_repeat)])
        menu_top.update(PygameUtils.center_joy())  # center !!
        self.assertEqual(menu.get_current()._joy_event, 0)

        # Active widget, and click outside to disable it (only if motion selection enabled)
        widg = menu.get_selected_widget()
        widg.active = True
        w_rect = widg.get_rect()

        # Clicking the same rect should not fire the callback
        menu_top.update([PygameUtils.middle_rect_click(w_rect, menu, evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertTrue(widg.active)
        self.assertTrue(widg.selected)

        w_rect.x += 500
        menu._mouse_motion_selection = True
        menu_top.update([PygameUtils.middle_rect_click(w_rect, menu, evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertFalse(widg.active)

    def test_enabled(self):
        """
        Test menu enable/disable feature.
        """
        menu = MenuUtils.generic_menu(onclose=events.NONE)
        self.assertTrue(not menu.is_enabled())
        menu.enable()
        self.assertTrue(menu.is_enabled())
        self.assertFalse(not menu.is_enabled())

        # Initialize and close
        menu.mainloop(surface, bgfun=dummy_function, disable_loop=True)
        menu._close()

    # noinspection PyArgumentEqualDefault
    def test_depth(self):
        """
        Test depth of a menu.
        """
        self.menu.clear()
        self.assertEqual(self.menu._get_depth(), 0)

        # Adds some menus
        menu_prev = self.menu
        menu = None
        for i in range(1, 11):
            menu = MenuUtils.generic_menu(title='submenu {0}'.format(i))
            button = menu_prev.add_button('open', menu)
            button.apply()
            menu_prev = menu
        self.menu.enable()
        self.menu.draw(surface)

        self.assertNotEqual(self.menu.get_current().get_id(), self.menu.get_id())
        self.assertTrue(self.menu != menu)
        self.assertEqual(menu._get_depth(), 10)
        self.assertEqual(self.menu._get_depth(), 10)

        """
        menu when it was opened it changed to submenu 1, when submenu 1 was opened
        it changed to submenu 2, and so on...
        """
        self.assertEqual(self.menu.get_title(), 'mainmenu')
        self.assertEqual(self.menu.get_current().get_title(), 'submenu 10')
        self.assertEqual(menu.get_current().get_title(), 'submenu 10')

        """
        Submenu 10 has not changed to any, so back will not affect it,
        but mainmenu will reset 1 unit
        """
        menu._back()
        self.assertEqual(menu.get_title(), 'submenu 10')

        """
        Mainmenu has changed, go back changes from submenu 10 to 9
        """
        self.assertEqual(self.menu._get_depth(), 9)
        self.menu._back()
        self.assertEqual(self.menu._get_depth(), 8)
        self.assertEqual(self.menu.get_title(), 'mainmenu')
        self.assertEqual(self.menu.get_current().get_title(), 'submenu 8')

        """
        Full go back (reset)
        """
        self.menu.full_reset()
        self.assertEqual(self.menu._get_depth(), 0)
        self.assertEqual(self.menu.get_current().get_title(), 'mainmenu')

    # noinspection PyArgumentEqualDefault
    def test_get_widget(self):
        """
        Tests widget status.
        """
        self.menu.clear()

        widget = self.menu.add_text_input('test', textinput_id='some_id')
        widget_found = self.menu.get_widget('some_id')
        self.assertEqual(widget, widget_found)

        # Add a widget to a deepest menu
        prev_menu = self.menu
        for i in range(11):
            menu = MenuUtils.generic_menu()
            prev_menu.add_button('menu', menu)
            prev_menu = menu

        # Add a deep input
        deep_widget = prev_menu.add_text_input('title', textinput_id='deep_id')
        deep_selector = prev_menu.add_selector('selector', [('0', 0), ('1', 1)], selector_id='deep_selector', default=1)

        self.assertEqual(self.menu.get_widget('deep_id', recursive=False), None)
        self.assertEqual(self.menu.get_widget('deep_id', recursive=True), deep_widget)
        self.assertEqual(self.menu.get_widget('deep_selector', recursive=True), deep_selector)

    def test_add_generic_widget(self):
        """
        Test generic widget.
        """
        self.menu.clear()
        menu = MenuUtils.generic_menu()
        btn = menu.add_button('nice', None)
        w = Button('title')
        self.menu.add_generic_widget(w)
        self.assertRaises(ValueError, lambda: menu.add_generic_widget(w))
        btn._menu = None
        self.menu.add_generic_widget(btn)

    # noinspection PyArgumentEqualDefault
    def test_get_selected_widget(self):
        """
        Tests get current widget.
        """
        self.menu.clear()

        # Test widget selection and removal
        widget = self.menu.add_text_input('test', default='some_id')
        self.assertEqual(widget, self.menu.get_selected_widget())
        self.menu.remove_widget(widget)
        self.assertEqual(self.menu.get_selected_widget(), None)
        self.assertEqual(self.menu.get_index(), -1)

        # Add two widgets, first widget will be selected first, but if removed the second should be selected
        widget1 = self.menu.add_text_input('test', default='some_id', textinput_id='epic')
        self.assertRaises(IndexError, lambda: self.menu.add_text_input('test', default='some_id', textinput_id='epic'))
        widget2 = self.menu.add_text_input('test', default='some_id')
        self.assertEqual(widget1.get_menu(), self.menu)
        self.assertEqual(widget1, self.menu.get_selected_widget())
        self.menu.remove_widget(widget1)
        self.assertEqual(widget1.get_menu(), None)
        self.assertEqual(widget2, self.menu.get_selected_widget())
        self.menu.remove_widget(widget2)
        self.assertEqual(widget2.get_menu(), None)
        self.assertEqual(len(self.menu.get_widgets()), 0)

        # Add 3 widgets, select the last one and remove it, then the selected widget must be the first
        w1 = self.menu.add_button('1', None)
        w2 = Label('2')
        self.menu.add_generic_widget(w2, configure_defaults=True)
        w3 = self.menu.add_button('3', None)
        self.assertEqual(self.menu.get_selected_widget(), w1)
        self.menu.select_widget(w3)
        self.assertEqual(self.menu.get_selected_widget(), w3)
        self.menu.remove_widget(w3)
        # 3 was deleted, so 1 should be selected
        self.assertEqual(self.menu.get_selected_widget(), w1)

        # Hides w1, then w2 should be selected
        w1.hide()
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Unhide w1, w2 should be keep selected
        w1.show()
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Mark w1 as unselectable and remove w2, then no widget should be selected
        w1.is_selectable = False
        self.menu.remove_widget(w2)
        self.assertEqual(self.menu.get_selected_widget(), None)
        self.assertRaises(ValueError, lambda: self.menu.select_widget(w1))

        # Mark w1 as selectable
        w1.is_selectable = True
        self.menu.add_generic_widget(w2)
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Add a new widget that cannot be selected
        self.menu.add_label('not selectable')
        self.menu.add_label('not selectable')
        w_last = self.menu.add_label('not selectable', selectable=True)

        # If w2 is removed, then menu will try to select labels, but as them are not selectable it should select the last one
        w2.hide()
        self.assertEqual(self.menu.get_selected_widget(), w_last)

        # Mark w1 as unselectable, then w1 is not selectable, nor w2, and labels are unselectable too
        # so the selected should be the same
        w1.is_selectable = False
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(self.menu.get_selected_widget(), w_last)

        # Show w2, then if DOWN is pressed again, the selected status should be 2
        w2.show()
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Hide w2, pass again to w_last
        w2.hide()
        self.assertEqual(self.menu.get_selected_widget(), w_last)

        # Hide w_last, then nothing is selected
        w_last.hide()
        self.assertEqual(self.menu.get_selected_widget(), None)

        # Unhide w2, then it should be selected
        w2.show()
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Remove w2, then nothing should be selected
        self.menu.remove_widget(w2)
        self.assertEqual(self.menu.get_selected_widget(), None)

        # Clear all widgets and get index
        self.menu._widgets = []
        self._index = 100
        self.assertEqual(self.menu.get_selected_widget(), None)

        # Destroy index
        self.menu._index = '0'
        self.assertEqual(None, self.menu.get_selected_widget())
        self.assertEqual(self.menu._index, 0)

    def test_submenu(self):
        """
        Test submenus.
        """
        menu = MenuUtils.generic_menu()
        menu2 = MenuUtils.generic_menu()
        btn = menu.add_button('btn', menu2)
        self.assertTrue(btn.to_menu)
        self.assertTrue(menu.in_submenu(menu2))
        self.assertFalse(menu2.in_submenu(menu))

        btn.update_callback(lambda: None)
        self.assertFalse(btn.to_menu)
        self.assertFalse(menu.in_submenu(menu2))

        # Test recursive
        menu.clear()
        menu2.clear()

        self.assertRaises(ValueError, lambda: menu.add_button('to self', menu))
        menu.add_button('to2', menu2)
        self.assertRaises(ValueError, lambda: menu2.add_button('to1', menu))

    def test_centering(self):
        """
        Test centering menu.
        """
        # Vertical offset disables centering
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.widget_offset = (0, 100)
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertEqual(menu.get_theme(), theme)
        self.assertFalse(menu._center_content)

        # Outer scrollarea margin disables centering
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.scrollarea_outer_margin = (0, 100)
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertFalse(menu._center_content)

        # Normal
        theme = pygame_menu.themes.THEME_BLUE.copy()
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertTrue(menu._center_content)

        # Text offset
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_font_size = 35
        theme.widget_font_size = 25

        menu = pygame_menu.Menu(
            title='test',
            height=300,
            theme=theme,
            width=400,
            overflow=False
        )

        menu.add_label('Text #1')
        menu.add_vertical_margin(100)
        menu.add_label('Text #2')
        v = 36
        if pygame.version.vernum[0] < 2:
            v = 35

        self.assertEqual(menu._widget_offset[1], v)

    def test_getters(self):
        """
        Test other getters.
        """
        self.assertTrue(self.menu.get_menubar_widget() is not None)
        self.assertTrue(self.menu.get_scrollarea() is not None)

        w, h = self.menu.get_size()
        self.assertEqual(int(w), 600)
        self.assertEqual(int(h), 400)

        w, h = self.menu.get_window_size()
        self.assertEqual(int(w), 600)
        self.assertEqual(int(h), 600)

    def test_generic_events(self):
        """
        Test key events.
        """
        self.menu.clear()

        # Add a menu and a method that set a function
        event_val = [False]

        def _some_event():
            event_val[0] = True
            return 'the value'

        # Add some widgets
        button = None
        wid = []
        for i in range(5):
            button = self.menu.add_button('button', _some_event)
            wid.append(button.get_id())
        self.assertEqual(len(self.menu.get_widgets()), 5)

        # Create a event in pygame
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(self.menu.get_index(), 1)

        # Move down twice
        for i in range(2):
            self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(self.menu.get_index(), 4)
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(self.menu.get_index(), 0)

        # Press enter, button should trigger and call function
        self.assertEqual(button.apply(), 'the value')
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_APPLY, keydown=True))

        # Other
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_CLOSE_MENU, keydown=True))
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_BACK, keydown=True))

        # Check index is the same as before
        self.assertEqual(self.menu.get_index(), 0)

        # Check joy
        self.menu.update(PygameUtils.joy_key(pygame_menu.controls.JOY_UP))
        self.assertEqual(self.menu.get_index(), 4)
        self.menu.update(PygameUtils.joy_key(pygame_menu.controls.JOY_DOWN))
        self.assertEqual(self.menu.get_index(), 0)
        self.menu.update(PygameUtils.joy_motion(1, 1))
        self.assertEqual(self.menu.get_index(), 1)
        self.menu.update(PygameUtils.joy_motion(1, -1))
        self.assertEqual(self.menu.get_index(), 0)
        self.menu.update(PygameUtils.joy_motion(1, -1))
        self.assertEqual(self.menu.get_index(), 4)

        click_pos = PygameUtils.get_middle_rect(button.get_rect())
        self.menu.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))
        self.assertTrue(event_val[0])
        event_val[0] = False

    def test_back_event(self):
        """
        Test back event.
        """
        self.menu.clear()
        self.assertEqual(self.menu._get_depth(), 0)
        menu = MenuUtils.generic_menu(title='submenu')
        button = self.menu.add_button('open', menu)
        button.apply()
        self.assertEqual(self.menu._get_depth(), 1)
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_BACK, keydown=True))  # go back
        self.assertEqual(self.menu._get_depth(), 0)

    def test_mouse_empty_submenu(self):
        """
        Test mouse event where the following submenu has less elements.
        """
        self.menu.clear()
        self.menu.enable()

        submenu = MenuUtils.generic_menu()  # 1 option
        submenu.add_button('button', lambda: None)

        self.menu.add_button('button', lambda: None)
        self.menu.add_button('button', lambda: None)
        button = self.menu.add_button('button', submenu)
        self.menu.disable()
        self.assertRaises(RuntimeError, lambda: self.menu.draw(surface))
        self.menu.enable()
        self.menu.draw(surface)

        click_pos = PygameUtils.get_middle_rect(button.get_rect())
        self.menu.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))

    def test_input_data(self):
        """
        Test input data gathering.
        """
        self.menu.clear()

        self.menu.add_text_input('text1', textinput_id='id1', default=1)  # Force to string
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id1'], '1')

        self.menu.add_text_input('text1', textinput_id='id2', default=1.5, input_type=pygame_menu.locals.INPUT_INT)
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id2'], 1)  # Cast to int
        self.assertRaises(IndexError, lambda: self.menu.add_text_input('text1', textinput_id='id1', default=1))

        self.menu.add_text_input('text1', textinput_id='id3', default=1.5, input_type=pygame_menu.locals.INPUT_FLOAT)
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id3'], 1.5)  # Correct

        # Add input to a submenu
        submenu = MenuUtils.generic_menu()
        submenu.add_text_input('text', textinput_id='id4', default='thewidget')
        self.menu.add_button('submenu', submenu)
        data = self.menu.get_input_data(recursive=True)
        self.assertEqual(data['id4'], 'thewidget')

        # Add a submenu within submenu with a repeated id, menu.get_input_data
        # should raise an exception
        subsubmenu = MenuUtils.generic_menu()
        # noinspection SpellCheckingInspection
        subsubmenu.add_text_input('text', textinput_id='id4', default='repeateddata')
        submenu.add_button('submenu', subsubmenu)
        self.assertRaises(ValueError, lambda: self.menu.get_input_data(recursive=True))

    def test_columns_menu(self):
        """
        Test menu columns behaviour.
        """
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=-1))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(rows=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(rows=-10))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=2, rows=0))

        # Assert append more widgets than number of rows*columns
        _column_menu = MenuUtils.generic_menu(columns=2, rows=4)
        for _ in range(8):
            _column_menu.add_button('test', pygame_menu.events.BACK)
        _column_menu.mainloop(surface, bgfun=dummy_function)
        _column_menu._left()
        _column_menu._right()
        _column_menu.disable()
        self.assertRaises(RuntimeError, lambda: _column_menu.draw(surface))
        _column_menu.enable()
        _column_menu.draw(surface)
        _column_menu.disable()
        self.assertRaises(RuntimeError, lambda: _column_menu.draw(surface))
        self.assertRaises(AssertionError, lambda: _column_menu.add_button('test', pygame_menu.events.BACK))  # 9th item

    def test_touchscreen(self):
        """
        Test menu touchscreen behaviour.
        """
        v_major, _, _ = pygame.version.vernum
        if v_major < 2:
            return

        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(title='mainmenu', touchscreen_enabled=False,
                                                                         touchscreen_motion_selection=True))
        menu = MenuUtils.generic_menu(title='mainmenu', touchscreen_enabled=True)
        menu.mainloop(surface, bgfun=dummy_function)

        # Add a menu and a method that set a function
        event_val = [False]

        def _some_event():
            event_val[0] = True
            return 'the value'

        # Add some widgets
        button = menu.add_button('button', _some_event)

        # Check touch
        click_pos = PygameUtils.get_middle_rect(button.get_rect())
        menu.update(PygameUtils.touch_click(click_pos[0], click_pos[1], normalize=False))  # Event must be normalized
        self.assertFalse(event_val[0])

        menu.update(PygameUtils.touch_click(click_pos[0], click_pos[1], menu=menu))
        self.assertTrue(event_val[0])
        event_val[0] = False
        self.assertEqual(menu.get_selected_widget().get_id(), button.get_id())
        btn = menu.get_selected_widget()  # type: Button
        self.assertTrue(btn.get_selected_time() >= 0)

    # noinspection PyArgumentList
    def test_invalid_args(self):
        """
        Test menu invalid args.
        """
        self.assertRaises(TypeError,
                          lambda: pygame_menu.Menu(height=100, width=100, title='nice', fake_option=True))

    def test_set_title(self):
        """
        Test menu title.
        """
        menu = MenuUtils.generic_menu(title='menu')
        theme = menu.get_theme()
        menubar = menu.get_menubar_widget()

        self.assertEqual(menu.get_title(), 'menu')
        self.assertEqual(menubar.get_title_offset()[0], theme.title_offset[0])
        self.assertEqual(menubar.get_title_offset()[1], theme.title_offset[1])

        menu.set_title('nice')
        self.assertEqual(menu.get_title(), 'nice')
        self.assertEqual(menubar.get_title_offset()[0], theme.title_offset[0])
        self.assertEqual(menubar.get_title_offset()[1], theme.title_offset[1])

        menu.set_title('nice', offset=(9, 10))
        self.assertEqual(menu.get_title(), 'nice')
        self.assertEqual(menubar.get_title_offset()[0], 9)
        self.assertEqual(menubar.get_title_offset()[1], 10)

        menu.set_title('nice2')
        self.assertEqual(menu.get_title(), 'nice2')
        self.assertEqual(menubar.get_title_offset()[0], theme.title_offset[0])
        self.assertEqual(menubar.get_title_offset()[1], theme.title_offset[1])

    def test_visible(self):
        """
        Test visible.
        """
        menu = MenuUtils.generic_menu(title='menu')
        btn1 = menu.add_button('nice', None)
        btn2 = menu.add_button('nice', None)
        self.assertTrue(btn1.selected)
        btn2.hide()
        menu.select_widget(btn1)

        # btn2 cannot be selected as it is hidden
        self.assertRaises(ValueError, lambda: menu.select_widget(btn2))
        btn2.show()
        menu.select_widget(btn2)

        # Hide buttons
        btn1.hide()
        btn2.hide()

        self.assertFalse(btn1.selected)
        self.assertFalse(btn2.selected)

        menu = MenuUtils.generic_menu(title='menu')
        btn = menu.add_button('button', None)
        self.assertTrue(btn.selected)
        btn.hide()

        # As theres no more visible widgets, index must be -1
        self.assertEqual(menu._index, -1)
        self.assertFalse(btn.selected)
        btn.show()

        # Widget should be selected, and index must be 0
        self.assertTrue(btn.selected)
        self.assertEqual(menu._index, 0)

        # Hide button, and set is as unselectable
        btn.hide()
        btn.is_selectable = False
        self.assertEqual(menu._index, -1)
        btn.show()

        # Now, as widget is not selectable, button should not
        # be selected and index still -1
        self.assertFalse(btn.selected)
        self.assertEqual(menu._index, -1)

        # Set selectable again
        btn.is_selectable = True
        btn.set_selected()
        self.assertEqual(menu._index, -1)  # Menu still don't considers widget as selected
        self.assertEqual(menu.get_selected_widget(), None)
        btn.set_selected()
        menu.select_widget(btn)
        self.assertEqual(menu.get_selected_widget(), btn)

    def test_focus(self):
        """
        Test menu focus effect.
        """
        menu = MenuUtils.generic_menu(title='menu', mouse_motion_selection=True)
        btn = menu.add_button('nice', None)

        # Test focus
        btn.active = True
        focus = menu._draw_focus_widget(surface, btn)
        self.assertEqual(len(focus), 4)
        if pygame.version.vernum[0] < 2:
            self.assertEqual(focus[1], ((0, 0), (600, 0), (600, 301), (0, 301)))
            self.assertEqual(focus[2], ((0, 302), (261, 302), (261, 353), (0, 353)))
            self.assertEqual(focus[3], ((337, 302), (600, 302), (600, 353), (337, 353)))
            self.assertEqual(focus[4], ((0, 354), (600, 354), (600, 600), (0, 600)))
        else:
            self.assertEqual(focus[1], ((0, 0), (600, 0), (600, 302), (0, 302)))
            self.assertEqual(focus[2], ((0, 303), (261, 303), (261, 353), (0, 353)))
            self.assertEqual(focus[3], ((337, 303), (600, 303), (600, 353), (337, 353)))
            self.assertEqual(focus[4], ((0, 354), (600, 354), (600, 600), (0, 600)))

        # Test cases where the focus must fail
        btn.selected = False
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        btn.selected = True

        # Set active false
        btn.active = False
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        btn.active = True

        btn.hide()
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        btn.show()

        btn.is_selectable = False
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        btn.is_selectable = True

        menu._mouse_motion_selection = False
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        menu._mouse_motion_selection = True

        btn.active = True
        btn.selected = True
        self.assertNotEqual(None, menu._draw_focus_widget(surface, btn))

    def test_get_by_id(self):
        """
        Test get widget by id.
        """
        menu = MenuUtils.generic_menu()
        b1 = menu.add_button('1', None, button_id='1')
        b2 = menu.add_button('1', None, button_id='2')
        b3 = menu.add_button('1', None, button_id='3')
        self.assertEqual(menu.get_widget('2'), b2)
        self.assertIn(b2, menu.get_widgets())
        menu.remove_widget('2')
        self.assertNotIn(b2, menu.get_widgets())
        menu.select_widget('3')
        self.assertEqual(menu.get_selected_widget(), b3)
        menu.select_widget(b1)
