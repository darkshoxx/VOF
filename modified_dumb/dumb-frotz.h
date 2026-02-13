/* dumb-frotz.h
 * $Id: dumb-frotz.h,v 1.5 1998/07/08 03:45:40 al Exp $
 * Frotz os functions for a standard C library and a dumb terminal.
 * Now you can finally play Zork Zero on your Teletype.
 *
 * Copyright 1997, 1998 Alembic Petrofsky <alembic@petrofsky.berkeley.ca.us>.
 * Any use permitted provided this notice stays intact.
 */

extern int zargc;
extern int cwin;
extern int mwin;
extern int mouse_x;
extern int mouse_y;
extern int option_attribute_assignment;
extern int option_attribute_testing;
extern int option_object_locating;
extern int option_object_movement;
extern int option_context_lines;
extern int option_left_margin;
extern int option_right_margin;
extern int option_ignore_errors;
extern int option_piracy;
extern int option_undo_slots;
extern int option_expand_abbreviations;
extern int option_script_cols;


















#include "frotz.h"



















#include <stdio.h>



















#include <stdlib.h>



















#include <errno.h>



















#include <string.h>



















#include <ctype.h>



















#include <time.h>

/* From input.c.  */
bool is_terminator (zchar);

/* dumb-input.c */
bool dumb_handle_setting(const char *setting, bool show_cursor, bool startup);
void dumb_init_input(void);

/* dumb-output.c */
void dumb_init_output(void);
bool dumb_output_handle_setting(const char *setting, bool show_cursor,
				bool startup);
void dumb_show_screen(bool show_cursor);
void dumb_show_prompt(bool show_cursor, char line_type);
void dumb_dump_screen(void);
void dumb_display_user_input(char *);
void dumb_discard_old_input(int num_chars);
void dumb_elide_more_prompt(void);
void dumb_set_picture_cell(int row, int col, char c);

/* dumb-pic.c */
void dumb_init_pictures(char *graphics_filename);
