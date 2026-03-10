`timescale 1ns / 1ps

module tb_pipeline;

////////////////////////////////////////////////////////////
// CLOCK & RESET
////////////////////////////////////////////////////////////
reg clk;
reg reset;

// 100 MHz clock
initial begin
   clk = 0;
   forever #5 clk = ~clk;
end

// Reset sequence (active low based on your initial block)
initial begin
   reset = 0;
   #100;
   reset = 1;
end


////////////////////////////////////////////////////////////
// INTERCONNECT WIRES (Declared to connect DUT to Memories)
////////////////////////////////////////////////////////////

// Instruction Memory interconnects
wire [31:0] inst_mem_read_data;
wire        inst_mem_is_valid = 1'b1;
wire [31:0] inst_mem_address;
wire [31:0] inst_fetch_pc;

// Data Memory interconnects
wire [31:0] dmem_read_data;
wire        dmem_write_valid = 1'b1;
wire        dmem_read_valid  = 1'b1;
wire        dmem_read_ready;
wire [31:0] dmem_read_address;
wire        dmem_write_ready;
wire [31:0] dmem_write_addr;
wire [31:0] dmem_write_data;
wire [3:0]  dmem_write_byte;

// CPU Status interconnects
wire        exception;
wire [31:0] pc_out;


////////////////////////////////////////////////////////////
// DUT : PIPELINE CPU
////////////////////////////////////////////////////////////
pipe DUT (
   .clk(clk),
   .reset(reset),
   .stall(1'b0),
   .exception(exception),
   .pc_out(pc_out),

   // Instruction Memory Interface
   .inst_mem_is_valid(inst_mem_is_valid),
   .inst_mem_read_data(inst_mem_read_data),
   .inst_mem_address(inst_mem_address),
   .inst_fetch_pc(inst_fetch_pc),

   // Data Memory Interface
   .dmem_read_data_temp(dmem_read_data),
   .dmem_write_valid(dmem_write_valid),
   .dmem_read_valid(dmem_read_valid),
   .dmem_read_ready(dmem_read_ready),
   .dmem_read_address(dmem_read_address),
   .dmem_write_ready(dmem_write_ready),
   .dmem_write_addr(dmem_write_addr),
   .dmem_write_data(dmem_write_data),
   .dmem_write_byte(dmem_write_byte)
);


////////////////////////////////////////////////////////////
// INSTRUCTION MEMORY 
////////////////////////////////////////////////////////////
instr_mem IMEM (
   .clk(clk),
   .pc(inst_mem_address),
   .instr(inst_mem_read_data)
);


////////////////////////////////////////////////////////////
// DATA MEMORY 
////////////////////////////////////////////////////////////
data_mem DMEM (
   .clk(clk),

   .re(dmem_read_ready),
   .raddr(dmem_read_address),
   .rdata(dmem_read_data),

   .we(dmem_write_ready),
   .waddr(dmem_write_addr),
   .wdata(dmem_write_data),
   .wstrb(dmem_write_byte)
);


////////////////////////////////////////////////////////////
// SIMULATION TIME & WAVEFORM DUMPING
////////////////////////////////////////////////////////////
initial begin
   // Enable waveform generation to view in GTKWave / ModelSim
   $dumpfile("pipeline_waveforms.vcd");
   $dumpvars(0, tb_pipeline);
   
   #20000;   // run long enough to see program execute
   $finish;
end

endmodule