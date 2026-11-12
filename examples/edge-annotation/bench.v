// SPDX-License-Identifier: Apache-2.0
`timescale 1ns/1ps
`include "helper.v"
`include "model.v"
`timescale 1ps/1ps
module bench;
  reg s, i0, i1;
  wire z;
  gf180mcu_fd_sc_mcu7t5v0__mux2_2 dut(.S(s), .I0(i0), .I1(i1), .Z(z));
  initial begin
    $sdf_annotate("first.sdf", dut);
    $path_snapshot("first", dut);
    $sdf_annotate("records.sdf", dut);
    $path_snapshot("final", dut);
    #1000; s=0; i0=0; i1=1;
    #9000; s=1;
    #10000; s=0;
    #10000; i0=1; i1=0;
    #10000; s=1;
    #10000; s=0;
    #10000; $display("END %0d", $time);
  end
  always @(z) $display("PIN Z %0d %b", $time, z);
  always @(s) $strobe("SOURCE S %0d %b%b%b", $time, s,i0,i1);
endmodule
