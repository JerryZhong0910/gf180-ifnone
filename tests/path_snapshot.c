/* SPDX-License-Identifier: Apache-2.0 */
/* Read actual compiled paths and both effective output-transition slots. */
#include <stdio.h>
#include "vpi_user.h"

static PLI_INT32 snapshot(PLI_BYTE8 *unused)
{
    (void)unused;
    vpiHandle call = vpi_handle(vpiSysTfCall, 0);
    vpiHandle args = vpi_iterate(vpiArgument, call);
    s_vpi_value value = { .format = vpiStringVal };
    vpi_get_value(vpi_scan(args), &value);
    const char *label = value.value.str;
    vpiHandle scope = vpi_scan(args);
    vpi_free_object(args);
    vpiHandle paths = vpi_iterate(vpiModPath, scope), path;
    while (paths && (path = vpi_scan(paths))) {
        vpiHandle input = vpi_handle(vpiModPathIn, path);
        vpiHandle output = vpi_handle(vpiModPathOut, path);
        s_vpi_time times[2];
        s_vpi_delay delay = { .da = times, .no_of_delays = 2,
            .time_type = vpiScaledRealTime, .mtm_flag = 0,
            .append_flag = 0, .pulsere_flag = 0 };
        vpi_get_delays(path, &delay);
        /* vpi_get_str uses shared storage: print each value before another call. */
        vpi_printf("PATH %s ", label);
        vpi_printf("%s %d ", vpi_get_str(vpiFullName, scope), vpi_get(vpiEdge, input));
        vpi_printf("%s ", vpi_get_str(vpiName, vpi_handle(vpiExpr, input)));
        vpi_printf("%s ", vpi_get_str(vpiName, vpi_handle(vpiExpr, output)));
        const char *condition = vpi_get_str(_vpiModPathCondition, path);
        vpi_printf("%s %.12g %.12g\n", condition && *condition ? condition : "-",
                   times[0].real, times[1].real);
    }
    return 0;
}
static void register_snapshot(void)
{
    s_vpi_systf_data task = { .type = vpiSysTask, .tfname = "$path_snapshot",
        .calltf = snapshot, .compiletf = 0, .sizetf = 0, .user_data = 0 };
    vpi_register_systf(&task);
}
void (*vlog_startup_routines[])(void) = { register_snapshot, 0 };
