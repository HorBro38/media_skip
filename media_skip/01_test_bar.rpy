python early:
    from renpy.display.render import render

    class ThumbBar(Bar):
        def render(self, width, height, st, at):

            # Handle redrawing.
            if self.value is not None:
                redraw = self.value.periodic(st)

                if redraw is not None:
                    renpy.display.render.redraw(self, redraw)

            xminimum, yminimum = renpy.display.layout.xyminimums(self.style, width, height)

            if xminimum is not None:
                width = max(width, xminimum)

            if yminimum is not None:
                height = max(height, yminimum)

            # Store the width and height for the event function to use.
            self.width = width
            self.height = height
            range = self.adjustment.range # @ReservedAssignment
            value = self.adjustment.value
            page = self.adjustment.page

            if range <= 0:
                if self.style.unscrollable == "hide":
                    self.hidden = True
                    return renpy.display.render.Render(width, height)
                elif self.style.unscrollable == "insensitive":
                    self.set_style_prefix("insensitive_", True)
            else:
                if self.style.prefix == "insensitive_":
                    self.set_style_prefix("idle_", True)

            self.hidden = False

            if self.style.bar_invert ^ self.style.bar_vertical:
                value = range - value

            bar_vertical = self.style.bar_vertical

            if bar_vertical:
                dimension = height
            else:
                dimension = width

            fore_gutter = self.style.fore_gutter
            aft_gutter = self.style.aft_gutter

            active = dimension - fore_gutter - aft_gutter
            if range:
                thumb_dim = active * page // (range + page)
            else:
                thumb_dim = active

            if isinstance(self.style.thumb_offset, tuple):
                fore_thumb_offset = abs(self.style.thumb_offset[0])
                aft_thumb_offset = abs(self.style.thumb_offset[1])
            else:
                fore_thumb_offset = abs(self.style.thumb_offset)
                aft_thumb_offset = fore_thumb_offset

            if bar_vertical:
                thumb = render(self.style.thumb, width, thumb_dim, st, at)
                thumb_shadow = render(self.style.thumb_shadow, width, thumb_dim, st, at)
                thumb_dim = thumb.height
            else:
                thumb = render(self.style.thumb, thumb_dim, height, st, at)
                thumb_shadow = render(self.style.thumb_shadow, thumb_dim, height, st, at)
                thumb_dim = thumb.width

            # Remove the offset from the thumb.
            thumb_dim -= fore_thumb_offset + aft_thumb_offset
            self.thumb_dim = thumb_dim

            active -= thumb_dim

            if range:
                fore_size = active * value // range
            else:
                fore_size = active

            fore_size = int(fore_size)

            aft_size = active - fore_size

            fore_size += fore_gutter
            aft_size += aft_gutter

            rv = renpy.display.render.Render(width, height)

            if bar_vertical:

                if self.style.bar_resizing:
                    foresurf = render(self.style.fore_bar, width, fore_size, st, at)
                    aftsurf = render(self.style.aft_bar, width, aft_size, st, at)
                    rv.blit(thumb_shadow, (0, fore_size - fore_thumb_offset))
                    rv.blit(foresurf, (0, 0), main=False)
                    rv.blit(aftsurf, (0, height - aft_size), main=False)
                    rv.blit(thumb, (0, fore_size - fore_thumb_offset))

                else:
                    foresurf = render(self.style.fore_bar, width, height, st, at)
                    aftsurf = render(self.style.aft_bar, width, height, st, at)

                    rv.blit(thumb_shadow, (0, fore_size - fore_thumb_offset))
                    rv.blit(foresurf.subsurface((0, 0, width, fore_size)), (0, 0), main=False)
                    rv.blit(aftsurf.subsurface((0, height - aft_size, width, aft_size)), (0, height - aft_size), main=False)
                    rv.blit(thumb, (0, fore_size - fore_thumb_offset))

            else:
                if self.style.bar_resizing:
                    foresurf = render(self.style.fore_bar, fore_size, height, st, at)
                    aftsurf = render(self.style.aft_bar, aft_size, height, st, at)
                    rv.blit(thumb_shadow, (fore_size - fore_thumb_offset, 0))
                    rv.blit(foresurf, (0, 0), main=False)
                    rv.blit(aftsurf, (width - aft_size, 0), main=False)
                    rv.blit(thumb, (fore_size - fore_thumb_offset, 0))

                else:
                    foresurf = render(self.style.fore_bar, width, height, st, at)
                    aftsurf = render(self.style.aft_bar, width, height, st, at)

                    rv.blit(thumb_shadow, (fore_size - fore_thumb_offset, 0))
                    rv.blit(foresurf.subsurface((0, 0, fore_size, height)), (0, 0), main=False)
                    rv.blit(aftsurf.subsurface((width - aft_size, 0, aft_size, height)), (width - aft_size, 0), main=False)
                    rv.blit(thumb, (fore_size - fore_thumb_offset, 0))

            if self.focusable:
                rv.add_focus(self, None, 0, 0, width, height)

            return rv


    renpy.register_sl_displayable("thumb_bar", ThumbBar, "bar", 0, replaces=True,
        pass_context=True
        ).add_property("hovered"
        ).add_property("unhovered"
        ).add_property("update_interval"
        ).add_property("adjustment"
        ).add_property("range"
        ).add_property("value"
        ).add_property("changed"
        ).add_property("released"
        ).add_property("activate_sound"
        ).add_property("hover_sound"
        ).add_property_group("bar")
