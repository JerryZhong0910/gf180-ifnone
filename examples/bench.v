// SPDX-License-Identifier: Apache-2.0
`timescale 1ps/1ps
module bench;
  reg a, b, ci, i0, i1, i2, i3, s0, s1;
  wire sum, carry, z;
  gf180mcu_fd_sc_mcu9t5v0__addf_1 adder (.A(a), .B(b), .CI(ci), .S(sum), .CO(carry));
  gf180mcu_fd_sc_mcu9t5v0__mux4_2 mux (.I0(i0), .I1(i1), .I2(i2), .I3(i3), .S0(s0), .S1(s1), .Z(z));
  initial begin
    $sdf_annotate_initial("addf/converted.sdf", adder);
    $sdf_annotate_initial("mux4/converted.sdf", mux);
    $display("ANNOTATION_RETURNED %0d", $time);
    #1000;
    a=0; b=0; ci=0;
    i0=1; i1=1; i2=0; i3=1; s1=1; s0=0;
    #9000; a=1; s0=1;
    #20000; s0=0; i0=0; i1=1; i2=1'bx; i3=0; s1=0;
    #20000; s0=1;
    #20000; s0=0;
    #10000; $display("END %0d", $time);
  end
  always @(adder.S) $display("PIN S %0d %b", $time, adder.S);
  always @(mux.Z) $display("PIN Z %0d %b", $time, mux.Z);
  always @(adder.A) $strobe("SOURCE A %0d %b%b%b", $time, adder.A, adder.B, adder.CI);
  always @(mux.S0) $strobe("SOURCE S0 %0d %b%b%b%b%b%b", $time,
                            mux.S0, mux.S1, mux.I0, mux.I1, mux.I2, mux.I3);
  `include "predicate_probes.vh"
endmodule
