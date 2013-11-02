#!/usr/bin/env ruby
# -*- coding: utf-8 -*-

################################################################################
# default
################################################################################
@file = "prob2.txt"
@x = 5
@y = 7
@@debug = false

################################################################################
# Constant
################################################################################
@@empty = '_'
@@up    = 0
@@right = 1
@@down  = 2
@@left  = 3

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
  opts.on("-f [INPUT]"){ |f|
    @file = f
  }
  opts.on("-d", "--debug"){
    @@debug = true
  }
  # parse
  opts.parse!(ARGV)
}

################################################################################
# Class
################################################################################
########################################
# Cat
########################################
class MyCat
  #### new ####
  def initialize
    @name = ""
    @x = 0
    @y = 0
    @d = 0
  end
  attr_accessor :name, :x, :y, :d

  #### show ####
  def show
    puts "#{@name} @ [#{@x}, #{@y}] w/ #{@d}"
  end

  #### turn ####
  def turn(r)
    d = @d + r
    d = d + 4 if d < 0
    d = d - 4 if d >= 4
    face(d)
  end

  #### face ####
  def face(dir);  @d = dir; end

  #### walk ####
  def walk
    m = dir2move( @d )
    @x+= m[0]
    @y += m[1]
  end

  #### at? ####
  def at?(pos)
    @x == pos[0] && @y == pos[1]
  end
end

########################################
# Town
########################################
class MyTown
  ########################################
  # new, show, clone
  ########################################
  #### new ####
  def initialize(x, y, file)
    @x = x
    @y = y

    @town = Array.new(@x){ |x|  Array.new(@y){ |y| @@empty } }
    @goal = [0, 0]
    @b = MyCat.new # black cat
    @b.name = "black"
    @w = MyCat.new # white cat
    @w.name = "white"

    #### load ####
    open(file).each do |line|
      a = line.split
      x = a[0].to_i - 1
      y = a[1].to_i - 1
      v = a[2]

      if v == 'U' || v == 'D' || v == 'L' || v == 'R'
        @b.x = x
        @b.y = y
        @b.d = convert(v)
      elsif v == 'u' || v == 'd' || v == 'l' || v == 'r'
        @w.x = x
        @w.y = y
        @w.d = convert(v)
      elsif v == 'G'
        @goal = [x, y]
      else
        @town[x][y] = convert(v)
      end
    end
  end

  #### show ####
  def show
    puts "G = #{@goal}, B = [#{@b.x}, #{@b.y}], W = [#{@w.x}, #{@w.y}]"
    for x in 0..@x-1
      for y in 0..@y-1
        if @goal[0] == x && @goal[1] == y
          printf(" G")
        elsif @b.x == x && @b.y == y
          printf("%2s", @b.d)
        elsif @w.x == x && @w.y == y
          printf("%2s", @w.d)
        else
          printf("%2s", @town[x][y])
        end
      end
      printf("\n")
    end
  end

  ########################################
  # checker
  ########################################
  def hole?(c); @town[ c.x ][ c.y ] == 'H'; end
  def area?(c); 0 <= c.x && c.x < @x && 0 <= c.y && c.y < @y; end
  def goal?(c); c.at?(@goal); end

  ########################################
  # solver
  ########################################
  #### try ####
  def try(ary)
    last_a = nil
    ary.each do |dir|
      printf("Move for #{dir} ") if @@debug
      a = action(dir)

      #### for debug ####
      if @@debug
        case a
        when 0
          puts "--> Continue"
        when 1..2
          puts "--> Eate #{a} fish(es)"
        when 3
          puts "--> Goal"
        when -1
          puts "--> Fail"
        end
      end

      #### result ####
      case a
      when -1
        return -1
      when 3
        return 3
      end
      last_a = a
    end
    return last_a # last result
  end

  #### action = turn & walk ####
  def action(dir)
    r = dir - @b.d

    #### turn ####
    @b.turn(r)
    @w.turn(r)

    #### walk ####
    @b.walk
    @w.walk

    #### check ####
    return -1 if !area?(@b) || hole?(@b) || !area?(@w) || hole?(@w)
    return -1 if (!goal?(@b) && goal?(@w)) || (goal?(@b) && !goal?(@w))
    return 3  if goal?(@b) && goal?(@w)
    return -1 if @b.at?([@w.x, @w.y])

    #### eat ####
    eat(@b) + eat(@w)
  end

  #### eat ####
  def eat(c)
    #### find a fish ####
    dir = nil
    for d in 0..3
      m = dir2move(d)
      x = c.x + m[0]
      y = c.y + m[1]
      if 0 <= x && x < @x && 0 <= y && y < @y && @town[x][y] == 'F'
        dir = d
        break
      end
    end
    return 0 if dir == nil

    #### eat the fish ####
    c.face(dir)
    c.walk
    @town[c.x][c.y] = @@empty
    return 1
  end
end

########################################
# util
########################################
def move2dire(m)
  if x == -1 && y == 0
    return @@up
  elsif x == 1 && y == 0
    return @@down
  elsif x == 0 && y == -1
    return @@left
  elsif x == 0 && y == 1
    return @@right
  end
  -1
end
def dir2move(dir)
  x = 0
  y = 0
  case dir
  when @@up
    x = -1
  when @@down
    x = +1
  when @@left
    y = -1
  when @@right
    y = +1
  end
  [x, y]
end
def convert(char)
  case char
  when 'U'
    return @@up
  when 'u'
    return @@up
  when 'R'
    return @@right
  when 'r'
    return @@right
  when 'D'
    return @@down
  when 'd'
    return @@dow
  when 'L'
    return @@left
  when 'l'
    return @@left
  end
  char
end

################################################################################
# main
################################################################################
ds = [0, 1, 2, 3]
ps = [[]]
hs = [[]]

prev_length = 0
while ps.size > 0
  p = ps.shift
  h = hs.shift

  if p.size - prev_length == 1
    puts "level = #{p.size}"
  end
  prev_length = p.size

  ds.each do |d|
    puts "Try #{p + [d]}" if @@debug

    # try the path
    t = MyTown.new(@x, @y, @file)
    r = t.try(p + [d])
    case r
    when 0..2
      ps.push(p + [d])
      hs.push(h + [r])
    when 3
      puts "Solution = #{p + [d]}"
      exit(1)
    end
  end
end
