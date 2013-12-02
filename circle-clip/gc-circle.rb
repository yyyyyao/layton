#!/usr/bin/env ruby

################################################################################
# default
################################################################################
@pfile = "prb.txt"
@afile = "ans.txt"
@n = 100
@m = 30
@flag_g = false
@flag_c = false
PI = 3.14

################################################################################
# Arguments
################################################################################
require "optparse"
OptionParser.new { |opts|
  # options
  opts.on("-h","--help","Show this message") {
    puts opts
    exit
  }
  opts.on("-p [problem file]"){ |f|
    @pfile = f
  }
  opts.on("-a [answer file]"){ |f|
    @afile = f
    @flag_c = true
  }
  opts.on("-n [# points]"){ |f|
    @n = f.to_i
  }
  opts.on("-m [max. # circles]"){ |f|
    @m = f.to_i
  }
  opts.on("-G"){
    @flag_g = true
  }
  opts.on("-C"){
    @flag_c = true
  }
  # parse
  opts.parse!(ARGV)
}

################################################################################
# class
################################################################################
def random(_n); (rand * _n).to_i; end

########################################
# Circle
########################################
class Circle
  #### new ####
  def initialize(_x, _y, _r)
    @x = _x
    @y = _y
    @r = _r
  end

  #### show ####
  def show
    puts "#{@x} #{@y} #{@r} #{self.area}"
  end

  #### in? ####
  def in?(_x, _y)
    (@x - _x)**2 + (@y - _y) **2 < @r**2
  end

  #### area ####
  def area
    @r**2 * PI
  end
end

################################################################################
# main
################################################################################
if @flag_g
  f = open(@pfile, "w")
  f.puts @n
  f.puts @m
  for n in 1..@n
    f.puts "#{random(500)} #{random(500)}"
  end
  f.close
end

if @flag_c
  # load points
  f = open(@pfile)
  @ps = []
  @n = f.gets.to_i
  @m = f.gets.to_i
  for n in 1..@n
    line = f.gets
    ary = line.split.map{|i| i.to_i}
    @ps.push( ary )
  end
  f.close

  # load circles
  f = open(@afile)
  @cs = []
  @a  = 0
  @l = f.gets.to_i
  for l in 1..@l
    ary = f.gets.split.map{|i| i.to_i}
    x = ary[0]
    y = ary[1]
    z = ary[2]
    c = Circle.new(x, y, z)
    @cs.push(c)
  end

  #### total area ####
  @ta = 0
  @cs.each do |c|
    @ta += c.area
  end
  puts "total area = #{@ta / 500.0 ** 2}"

  #### check points ####
  @ps.each do |x, y|
    flag = false
    @cs.each do |c|
      if c.in?(x, y)
        flag = true
        break
      end
    end
    puts "(#{x}, #{y}) is uncovered." if !flag
  end
end
